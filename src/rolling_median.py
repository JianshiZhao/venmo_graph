# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 11:21:59 2016

@author: Jianshi
"""

import json
import sys
from datetime import datetime
throwaway = datetime.strptime('20110101','%Y%m%d')  


class VenmoGraph(object):
    '''
    Class to analyze Venmo users and their relationship with one another. Methods
    include building graph from Venmo transaction records, represented by a dictionary
    {node:[connections]}, storing and updating transactions within 60s timewindow,
    and calculate the median degree of a vertex. 
    '''
    def __init__(self,timewindow = 60.0):
        '''
        Set the sliding timewindow size in seconds. 
        Create a live_payments reservoir to store payments within the time window.
        '''
        self.timewindow = timewindow
        self.live_payments = []  # A list to store live transactions inside timewindow
    
    def is_valid(self, payment):
        '''
        Check if the payment record has both actor and target fields. 
        '''
        if (len(payment) ==3) and (payment['actor']!='') and (payment['target']!=''):
            return True
        else:
            return False

        
    def update_payments(self,new_payment):
        '''
        Given a new payment, update the payments within the time window. Remove payments
        outside the window.
        '''
        #check the current number of payments in the time window
        live_num = len(self.live_payments)
        pay_removel = [] # record the position of payment out of the time window
        UPDATE = True  # a flag used to show if the new payment is too old
        if live_num == 0:
            self.live_payments.append(new_payment)
        else:
            pay_time = datetime.strptime(new_payment['created_time'],'%Y-%m-%dT%H:%M:%SZ')
            # compare the create_time of the new payment with that of ones in the window
            for ind in range(live_num):
                cre_time = datetime.strptime(self.live_payments[ind]['created_time'],'%Y-%m-%dT%H:%M:%SZ')
                # select the indices of the ones with create_time 60s older than the new payment time                
                if (pay_time - cre_time).total_seconds() >= self.timewindow:
                    pay_removel.append(ind)
                # don't update the live_payments list if the new create_time is too old
                elif (pay_time - cre_time).total_seconds() <= (-self.timewindow):
                    UPDATE = False
                    break

            # remove the older payments from live_payments, and update the list if necessary
            if len(pay_removel)>0:
                newlist = [self.live_payments[n] for n in range(live_num) if n not in pay_removel]            
                self.live_payments = newlist
                
            if UPDATE:
                self.live_payments.append(new_payment)
        

    def create_graph(self,live_payments):
        '''
        Create a graph from the payments in the time window. Treat each actor and 
        target as a node in the graph. The graph is represented as a dictionary
        {node:[connections]}, where connections are unique neighbors of that node.
        '''
        graph = {}
        for ind in range(len(live_payments)):
            this_payment = live_payments[ind]
            if not graph.has_key(this_payment['actor']):
                graph[this_payment['actor']] = []
                graph[this_payment['actor']].append(this_payment['target'])
            else:
                graph[this_payment['actor']].append(this_payment['target'])
                graph[this_payment['actor']] = list(set(graph[this_payment['actor']])) 

            if not graph.has_key(this_payment['target']):
                graph[this_payment['target']] = []
                graph[this_payment['target']].append(this_payment['actor'])
            else:
                graph[this_payment['target']].append(this_payment['actor'])
                graph[this_payment['target']] = list(set(graph[this_payment['target']]))
        
        self.graph = graph

                
    def calculate_median(self,graph):
        degree = []
        for values in graph.values():
            degree.append(len(values))
        # sort the list    
        degree.sort() 
        len_deg = len(degree)
        # return the median
        if (len_deg % 2) == 0:
            return (degree[len_deg/2 - 1] + degree[len_deg/2])/2.0
        else:
            return degree[(len_deg-1)/2]
        
       

if __name__ == '__main__':
    
    try:
        venmo_input_file = sys.argv[1]
        venmo_output_file = sys.argv[2]
    except:
        print "Provide Filename! Or use as an imported module."
        venmo_input_file = raw_input("venmo_input file : \n")
        venmo_output_file = raw_input("venmo_output file: \n")

    venmo_input = open(venmo_input_file,'r')
    venmo_output = open(venmo_output_file,'w')
    
    venmo = VenmoGraph()    # Initilize an object
    for line in venmo_input:
        payment = json.loads(line) # read in one transaction
        try:                      
            if venmo.is_valid(payment):   
                # update payments within time window                  
                venmo.update_payments(payment)      
                # create graph from all payments within time window
                venmo.create_graph(venmo.live_payments)   
                # calculate median degree 
                median = venmo.calculate_median(venmo.graph)
                # write result to output file
                venmo_output.write(format(median,'.2f'))    
                venmo_output.write("\n")
            else:
                pass
        except Exception as e:
            print e
            
    venmo_input.close()
    venmo_output.close()    
