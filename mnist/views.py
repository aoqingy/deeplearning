import os
import re
import json
import base64
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data     # 导入mnist数据集

from mnist.logger import logger
from mnist.models import *

import deeplearning.settings as settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'mnist.html', {})


@csrf_exempt
def train(request):
    logger.info("Entering train...")

    try:
        mnist = input_data.read_data_sets(os.path.join(settings.BASE_DIR, 'mnist/MNIST_data'), one_hot=True)  # 下载数据
    
        # 设置权重weights和偏置biases作为优化变量，初始值设为0
        weights = tf.Variable(tf.zeros([784, 10]))
        biases = tf.Variable(tf.zeros([10]))

        # 构建模型
        x = tf.placeholder("float", [None, 784])
        y = tf.matmul(x, weights) + biases

        # 模型的预测值
        y_real = tf.placeholder("float", [None, 10])
        # 真实值
        cross_entropy = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_real, logits=y))

        # 预测值与真实值的交叉熵
        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

        # 使用梯度下降优化器最小化交叉熵
        # 开始训练
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for i in range(1000):
                batch_xs, batch_ys = mnist.train.next_batch(100)
                # 每次随机选取100个数据进行训练，即所谓的“随机梯度下降（Stochastic Gradient Descent，SGD）”
                sess.run(train_step, feed_dict={x: batch_xs, y_real:batch_ys})

                # 正式执行train_step，用feed_dict的数据取代placeholder
                if i % 1000 == 0:
                    # 每训练100次后评估模型
                    correct_prediction = tf.equal(tf.argmax(y, 1), tf.arg_max(y_real, 1))
                    # 比较预测值和真实值是否一致
                    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
                    # 统计预测正确的个数，取均值得到准确率
                    logger.info(sess.run(accuracy, feed_dict={x: mnist.test.images, y_real: mnist.test.labels}))

            logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            logger.info(sess.run(biases))
            saver = tf.train.Saver()
            saver.save(sess, "/tmp/mnist.ckpt")

            logger.info("Optimization Finished!")
            accuracy = sess.run(accuracy, feed_dict={x: mnist.test.images, y_real: mnist.test.labels})

        logger.info("Accuracy: %s" % accuracy)
        return HttpResponse(json.dumps({'code':'True', 'message':{'accuracy': str(accuracy)}}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))


def softmax(w):
    """Calculate the softmax of a list of numbers w.

    Parameters
    ----------
    w : list of numbers

    Return
    ------
    a list of the same length as w of non-negative numbers

    Examples
    --------
    >>> softmax([0.1, 0.2])
    array([ 0.47502081,  0.52497919])
    >>> softmax([-0.1, 0.2])
    array([ 0.42555748,  0.57444252])
    >>> softmax([0.9, -10])
    array([  9.99981542e-01,   1.84578933e-05])
    >>> softmax([0, 10])
    array([  4.53978687e-05,   9.99954602e-01])
    """
    e = np.exp(np.array(w))
    dist = e / np.sum(e)
    return dist


@csrf_exempt
def predict(request):
    logger.info("Entering predict...")
    data = request.POST.get('data', '')
    #logger.info('data: %s' % data)

    try:
        imgstr = re.search(r'base64,(.*)', data).group(1)
        output = open(os.path.join(settings.BASE_DIR, 'mnist/demo.png'), 'wb')
        output.write(base64.decodestring(imgstr.encode(encoding="utf-8")))
        output.close()

        img = Image.open(os.path.join(settings.BASE_DIR, 'mnist/demo.png'))
        img = img.resize((28,28))
        img.save(os.path.join(settings.BASE_DIR, 'mnist/demo-28.png'))

        img = Image.open(os.path.join(settings.BASE_DIR, 'mnist/demo-28.png'))
        #pix = img.load()
        width, height = img.size
        logger.info("width: %s, height: %s" % (str(width), str(height)))

        bits = []
        for i in range(height):
            for j in range(width):
                bits.append(float(img.getpixel((j,i))[3])/255.0)

        x_data = np.asarray(bits).reshape((28, 28))
        logger.info(x_data)
        x_data = np.asarray(bits).reshape((1, 784))

        # 设置权重weights和偏置biases作为优化变量，初始值设为0
        weights = tf.Variable(tf.zeros([784, 10]))
        biases = tf.Variable(tf.zeros([10]))

        # 构建模型
        x = tf.placeholder("float", [None, 784])
        y = tf.matmul(x, weights) + biases

        my_predict = ''
        with tf.Session() as sess:
            saver = tf.train.Saver()
            saver.restore(sess, "/tmp/mnist.ckpt")
            logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<")
            logger.info(sess.run(biases))

            y_data = sess.run(y, feed_dict={x: x_data})
            logger.info(y_data)
            y_data = sess.run(tf.nn.softmax(y), feed_dict={x: x_data})
            logger.info(y_data)

            for i in range(0, 10):
                if float(y_data[0][i]) > 0.1:
                    my_predict += str(i) + '......' + "{:.1f}".format(float(y_data[0][i]) * 100) + '%\n'

        logger.info('Done!')
        accuracy = 0.0
        return HttpResponse(json.dumps({'code':'True', 'message':{'predict': str(my_predict)}}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))

