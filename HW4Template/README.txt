Alyssa Hwang ahh2143
README for Introduction to Databases HW4 (NOSQL)

I provide a short description of the files I added/edited and how to run
the test cases. The files contained in this directory that are not discussed
in the README were provided by Professor Ferguson.

Make sure you have the SQL server, Redis, and Neo4j activated.

The HW4 directory contains the neo4j downloads.
The dbservice directory:
	dataservice.py contains the sample code/implementation
	dbservice1.png, dbservice2.png: screenshots of test output on console
	unit_test_ds.py: test cases for dataservice
	You can run the tests in the dbservice directory: python3 unit_test_ds.py
The redis_cache directory:
	data_cache.py contains the sample code/implementation
	redis.png: screenshot of test output on console
	unit_test.py: test cases for redis
	You can run the tests in the redis_cache directory: python3 unit_test.py
The social_graph directory:
	fan_comment_template.py: defines a fan comment
	socialgraph.png, socialgraph2.png, socialgraph3.png, socialgraph4.png:
	  screenshots of neo4j graph and test output on console
	unit_tests_local_social.py: test cases for social_graph
	You can run the tests in the social_graph directory:
	  python3 unit_tests_local_social.py

Most of the code is taken from Professor Ferguson's recitations.
