import json
import numpy as np
import tensorflow as tf
from logistic.logger import logger
from logistic.models import *

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



def index(request):
    return render(request, 'logistic.html', {})


@csrf_exempt
def listDots(request):
    logger.info("Entering listDots...")
    try:
        rdots = []
        for data in Data.objects.all():
            rdot = {}
            rdot['x1'] = data.dx1
            rdot['x2'] = data.dx2
            rdot['y']  = data.dy
            rdots.append(rdot)
        logger.info(rdots)
        return HttpResponse(json.dumps({'code':'True', 'message':rdots}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))


@csrf_exempt
def sampleDot(request):
    logger.info("Entering sampleDot...")
    x1 = request.POST.get('x1', '')
    x2 = request.POST.get('x2', '')
    y  = request.POST.get('y', '')
    logger.info('x1: %s, x2: %s, y: %s' % (x1, x2, y))

    try:
        data = Data(dx1=float(x1), dx2=float(x2), dy=int(y))
        data.save()
        logger.info('Done!')
        return HttpResponse(json.dumps({'code':'True', 'message':{'x1':x1, 'x2':x2, 'y':y}}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))


@csrf_exempt
def clearDots(request):
    logger.info("Entering clearDots...")
    try:
        for data in Data.objects.all():
            data.delete()
        logger.info('Done!')
        return HttpResponse(json.dumps({'code':'True', 'message':'Done!'}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))


@csrf_exempt
def trainDot(request):
    logger.info("Entering trainDot...")
    w1_data = request.POST.get('w1', '')
    w2_data = request.POST.get('w2', '')
    b_data  = request.POST.get('b', '')
    if not w1_data:
        w1_data = '0.0'
    if not w2_data:
        w2_data = '0.0'
    if not b_data:
        b_data = '0.0'
    logger.info('w1: %s, w2: %s, b: %s' % (w1_data, w2_data, b_data))

    try:
        learning_rate = 0.01
        training_epochs = 100
        display_step = 50

        # Training Data
        vlqs = Data.objects.values_list('dx1', 'dx2')
        train_X = np.asarray(vlqs)
        vlqs = Data.objects.values_list('dy')
        train_Y = np.asarray(vlqs)

        X = tf.placeholder(tf.float32, shape=[None, 2])
        Y = tf.placeholder(tf.float32, shape=[None, 1])

        W = tf.Variable(tf.random_normal([2,1]), dtype=tf.float32)
        b = tf.Variable(tf.random_normal([1]), dtype=tf.float32)
        W_assign = W.assign([[float(w1_data)], [float(w2_data)]])
        b_assign = b.assign([float(b_data)])

        # Construct a logistic model
        pred = tf.sigmoid(tf.matmul(X,W)+b)

        # Mean squared error
        cost = -tf.reduce_mean(Y*tf.log(pred)+(1-Y)*tf.log(1-pred))
        # Gradient descent
        # Note, minimize() knows to modify W and b because Variable objects are trainable=True by default
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

        # Initialize the variables (i.e. assign their default value)
        init = tf.global_variables_initializer()

        train_set = {X: train_X, Y: train_Y}

        # Start training
        with tf.Session() as sess:
            # Run the initializer
            sess.run(init)

            sess.run(W_assign)
            sess.run(b_assign)
            logger.info(sess.run(W[0][0]))
            logger.info(sess.run(W[1][0]))
            logger.info(sess.run(b[0]))

            # Fit all training data
            for epoch in range(training_epochs):
                #for (x, y) in zip(train_X, train_Y):
                #    sess.run(optimizer, feed_dict={X: x, Y: y})
                sess.run(optimizer, train_set)

                # Display logs per epoch step
                if (epoch+1) % display_step == 0:
                    #c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
                    c = sess.run(cost, train_set)
                    #logger.info("Epoch: %04d, cost: %s, W: %s, b: %s" % (epoch+1, "{:.9f}".format(c), "{:.9f}".format(sess.run(W)), "{:.9f}".format(sess.run(b))))

            logger.info("Optimization Finished!")
            training_cost = sess.run(cost, train_set)
            WW = sess.run(W)
            bb = sess.run(b)
            logger.info("Training cost: %s, w1: %s, w2: %s, b: %s" % (training_cost, WW[0][0], WW[1][0], bb[0]))

        logger.info('Done!')
        return HttpResponse(json.dumps({'code':'True', 'message':{'w1': str(WW[0][0]), 'w2': str(WW[1][0]), 'b': str(bb[0]), 'cost': str(training_cost)}}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))

