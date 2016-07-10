# Venmo Graph

##Program Summary

This program accomplished the following goals:

- Use Venmo payments that stream in to build a  graph of users and their relationship with one another.

- Calculate the median degree of a vertex in a graph and update this each time a new Venmo payment appears. The median degree is calculated across a 60-second sliding time window.

The vertices on the graph represent Venmo users and whenever one user pays another user, an edge is formed between the two users.


##Libraries and Modules
This program is written in Python 2.7, and uses severl basic modules including:
- json: this library is used to parses a tweet message written in JSON into a Python dictionary.
- sys : this library is used to catch the command line arguments, which specify the input and output file dictionaries.
- datetime : this librariy is used to compare time stamps for different tweets.

##Details of implementation

The file `venmo-trans.txt` contains the actual JSON messages with each payment on a newline. One example of the data for a single Venmo payment might look like:

<pre>
{"created_time": "2014-03-27T04:28:20Z", "target": "Jamie-Korn", "actor": "Jordan-Gruber"}
</pre>

The graph is represented by vertex and its neighbors. The number of connected neighbors for a vertex is the degree of a vertex. The graph and its associated median degree are updated each time a new payment is processed. The graph only consists of payments with timestamps that are 60 seconds or less from the maximum timestamp that has been processed.

##Test
This program has passed two indipendent tests using the provided insight testsuite. The test files are included in the insight_testsuite folder.

##Example
- To run the program: 
python average_degree.py tweet_input_file_path tweet_output_file_path

- Use as a module:

import average_degree

twitter = average_degree.twitter_graph() # create an twitter_graph object and use all the methods included

##Author
This program is written by Jianshi Zhao.  Any questions about this program can be sent to jszhaopsu at gmail.com