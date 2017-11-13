import tensorflow as tf

'''
input > weight > hidden layer 1 (activation function) > weights > hidden l 2  :
(activation function) > weights > output layer

compare output to intended output > cost or loss function (cross entropy)
optimization function (optimizer) > minimize cost (AdamOptimizer....SGD, AdaGrad)

backpropagation

feed forward + backprop = epoch
'''

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

# 10 classes, 0-9
'''
0 = [1,0,0,0,0,0,0,0,0,0]
1 = [0,1,0,0,0,0,0,0,0,0]
2 = [0,0,1,0,0,0,0,0,0,0]
'''

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 10
batch_size = 100

# height x width   28*28=784
x = tf.placeholder('float',[None, 784])
y = tf.placeholder('float')

def neural_network_model(data):

	# (input_data * weights) + biases

	hidden_1_layer = {'weights':tf.Variable(tf.random_normal([784, n_nodes_hl1])),
	                  'biases':tf.Variable(tf.random_normal([n_nodes_hl1]))}
    
	hidden_2_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
	                  'biases':tf.Variable(tf.random_normal([n_nodes_hl2]))}

	hidden_3_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
	                  'biases':tf.Variable(tf.random_normal([n_nodes_hl3]))}

	output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl2, n_classes])),
	                'biases':tf.Variable(tf.random_normal([n_classes]))}

	l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']) , hidden_1_layer['biases'])
	l1 = tf.nn.relu(l1)

	l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']) , hidden_2_layer['biases'])
	l2 = tf.nn.relu(l2)

	l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']) , hidden_3_layer['biases'])
	l3 = tf.nn.relu(l3)

	output = tf.matmul(l3,output_layer['weights']) + output_layer['biases']

	return output

def train_neural_network(x):
	prediction = neural_network_model(x)
	cost = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=y))
	#cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction,y) )
    #                            learning rate = 0.001
	optimizer = tf.train.AdamOptimizer().minimize(cost)
    
    #cycles feed forward + backprop
	hm_epochs = 10

	config = tf.ConfigProto(allow_soft_placement=True)
	gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
	#sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
	with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
		sess.run(tf.global_variables_initializer())

		for epoch in range(hm_epochs):
		    epoch_loss = 0
		    for _ in range(int(mnist.train.num_examples/batch_size)):
		    	epoch_x, epoch_y = mnist.train.next_batch(batch_size)
		    	_, c = sess.run([optimizer, cost], feed_dict={x: epoch_x,y: epoch_y})
		    	epoch_loss += c
		    print('Epoch', epoch, 'completed out of', hm_epochs,'loss:',epoch_loss)

		correct = tf.equal(tf.argmax(tf.argmax(prediction,1), tf.argmax(y,1)))

		accuracy = tf.reduce_mean(tf.cast(correct,'float'))
		#print('Accuracy:', accuracy.eval(x:mnist.test.images, y:mnist.test.labels))

train_neural_network(x)