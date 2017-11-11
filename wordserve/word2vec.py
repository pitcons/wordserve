from flask import current_app

import gensim
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors


# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack




class FlaskWord2Vec(object):

    _wv = {}

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('WORD2VEC_FILE', 'wordvectors.bin')
        app.config.setdefault('WORD2VEC_FILE_BINARY', True)
        app.config.setdefault('WORD2VEC_UNICODE_ERRORS', 'ignore')


        #import time

        #start = time.time()

        if app.config['IS_WORD2VEC_NATIVE']:
            self._wv[app.config['WORD2VEC_FILE']] = KeyedVectors.load_word2vec_format(
                app.config['WORD2VEC_FILE'],
                binary=app.config['WORD2VEC_FILE_BINARY'],
                unicode_errors=app.config['WORD2VEC_UNICODE_ERRORS']
            )
        else:
            self._wv[app.config['WORD2VEC_FILE']] = Word2Vec.load(
                app.config['WORD2VEC_FILE']
            )
        #end = time.time()

       # print(end-start)

        #print("init sims")

        #self._wv[app.config['WORD2VEC_FILE']].init_sims(replace=True)


    @property
    def word2vec(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, '_wv'):
                ctx._wv = self._wv[current_app.config['WORD2VEC_FILE']]
            return ctx._wv

w2v = FlaskWord2Vec()
