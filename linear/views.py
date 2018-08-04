import json
import numpy as np
import tensorflow as tf
from linear.logger import logger
from linear.models import *

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



def index(request):
    return render(request, 'example.html', {})


@csrf_exempt
def listDots(request):
    logger.info("Entering listDots...")
    try:
        rdots = []
        for axis in Axis.objects.all():
            rdot = {}
            rdot['x'] = axis.ax*100.0+1024/2
            rdot['y'] = axis.ay*100.0+768/2
            rdots.append(rdot)
        logger.info(rdots)
        return HttpResponse(json.dumps({'code':'True', 'message':rdots}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))


@csrf_exempt
def sampleDot(request):
    logger.info("Entering sampleDot...")
    x = request.POST.get('x', '')
    y = request.POST.get('y', '')
    logger.info('x: %s, y: %s' % (x, y))

    try:
        axis = Axis(ax=(float(x)-1024/2)/100.0, ay=(float(y)-768/2)/100.0)
        axis.save()
        logger.info('Done!')
        return HttpResponse(json.dumps({'code':'True', 'message':{'x':x, 'y':y}}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))


@csrf_exempt
def clearDots(request):
    logger.info("Entering clearDots...")
    try:
        for axis in Axis.objects.all():
            axis.delete()
        logger.info('Done!')
        return HttpResponse(json.dumps({'code':'True', 'message':'Done!'}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))


@csrf_exempt
def trainDot(request):
    logger.info("Entering trainDot...")
    WW = request.POST.get('W', '')
    bb = request.POST.get('b', '')
    if not WW:
        WW = '0.0'
    if not bb:
        bb = '0.0'
    logger.info('W: %s, b: %s' % (WW, bb))

    try:
        learning_rate = 0.01
        training_epochs = 200
        display_step = 50

        # Training Data
        vlqs = Axis.objects.values_list('ax', flat=True)
        train_X = np.asarray(vlqs)
        vlqs = Axis.objects.values_list('ay', flat=True)
        train_Y = np.asarray(vlqs)
        n_samples = train_X.shape[0]

        X = tf.placeholder("float")
        Y = tf.placeholder("float")

        W = tf.Variable(float(WW), name="weight")
        b = tf.Variable(float(bb), name="bias")

        # Construct a linear model
        pred = tf.add(tf.multiply(X, W), b)

        # Mean squared error
        cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
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

            # Fit all training data
            for epoch in range(training_epochs):
                #for (x, y) in zip(train_X, train_Y):
                #    sess.run(optimizer, feed_dict={X: x, Y: y})
                sess.run(optimizer, train_set)

                # Display logs per epoch step
                if (epoch+1) % display_step == 0:
                    #c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
                    c = sess.run(cost, train_set)
                    logger.info("Epoch: %04d, cost: %s, W: %s, b: %s" % (epoch+1, "{:.9f}".format(c), "{:.9f}".format(sess.run(W)), "{:.9f}".format(sess.run(b))))

            logger.info("Optimization Finished!")
            training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
            WW = sess.run(W)
            bb = sess.run(b)
            logger.info("Training cost: %s, W: %s, b: %s" % (training_cost, WW, bb))

        logger.info('Done!')
        return HttpResponse(json.dumps({'code':'True', 'message':{'W': str(WW), 'b': str(bb), 'cost': str(training_cost)}}))
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({'code':'False', 'message':str(e)}))

