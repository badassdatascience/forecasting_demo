#
# Load useful libraries
#
import tensorflow
from tensorflow.random import set_seed

from keras import layers
from keras.models import Sequential
from keras import regularizers
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam


class LSTM_Emily():

    def __init__(self, config):
        self.config = config
        self.build_generic_LSTM_regressor()
        self.compile_generic_regressor()

    def build_generic_LSTM_regressor(self):
        self.model = Sequential()

        #
        # build RNN layers (this will always produce at least one, optionally more)
        #
        for i, n_units_in_layer in enumerate(self.config['number_of_cells_per_RNN_layer_list']):

            if i == 0:
    
                #
                # define input layer
                #
                self.model.add(
                    layers.LSTM(
                        n_units_in_layer,
                        activation = self.config['lstm_activation_function'],
                        return_sequences = True,
                        input_shape = self.config['calculated_input_shape'],
                        #dropout = self.config['rnn_dropout_rate'],
                        recurrent_dropout = self.config['rnn_recurrent_dropout_rate'],
                    )
                )

            else:
                self.model.add(
                    layers.LSTM(
                        n_units_in_layer,
                        activation = self.config['lstm_activation_function'],
                        return_sequences = True,
                        #dropout = self.config['rnn_dropout_rate'],
                        recurrent_dropout = self.config['rnn_recurrent_dropout_rate'],
                    )
                )
        
        #
        # flatten
        #
        self.model.add(layers.Flatten())

        #
        # first batch normalization
        #
        self.model.add(layers.BatchNormalization(momentum = self.config['batch_normalization_momentum']))
    
        #
        # Build dense layers
        #
        for n_units_in_layer in self.config['number_of_cells_per_dense_layer_list']:
    
            self.model.add(
                layers.Dense(
                    n_units_in_layer,
                    activation = self.config['dense_activation_function'],

                    # https://keras.io/api/layers/regularizers/
                    kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4),
                    bias_regularizer=regularizers.L2(1e-4),
                    activity_regularizer=regularizers.L2(1e-5),
                )
            )

            self.model.add(layers.BatchNormalization(momentum = self.config['batch_normalization_momentum']))

            self.model.add(
                layers.Dropout(
                    rate = self.config['dense_dropout_rate'],
                )
            )
        
        #
        # define output layer
        #
        self.model.add(
            layers.Dense(
                self.config['calculated_number_of_outputs'],
                activation = self.config['final_dense_activation_function'],

                kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4),
                bias_regularizer=regularizers.L2(1e-4),
                activity_regularizer=regularizers.L2(1e-5),
            )
        )

    def compile_generic_regressor(self):
        self.model.compile(
            optimizer = Adam(learning_rate = self.config['learning_rate']),
            loss = self.config['loss_function'],
            metrics = self.config['metrics_to_store'],
        )

    def fit(self, train_X, train_y):

        #
        # set callbacks list
        #
        callbacks_list = [
            ReduceLROnPlateau(
                monitor = self.config['callbacks_dict']['ReduceLROnPlateau']['monitor'],
                factor = self.config['callbacks_dict']['ReduceLROnPlateau']['factor'],
                patience = self.config['callbacks_dict']['ReduceLROnPlateau']['patience'],
            ),
            ModelCheckpoint(
                filepath = self.config['checkpoint_file_path'],
                monitor = self.config['model_checkpoint_monitor'],
                save_best_only = self.config['model_checkpoint_save_best_only'],
            ),
        ]

        if self.config['use_variable_learning_rate']:
            self.history = self.model.fit(
                train_X,
                train_y,
                validation_split = self.config['validation_split'],
                epochs = self.config['epochs'],
                batch_size = self.config['batch_size'],
                callbacks = callbacks_list,
            )
        else:
            self.history = self.model.fit(
                train_X,
                train_y,
                validation_split = self.config['validation_split'],
                epochs = self.config['epochs'],
                batch_size = self.config['batch_size'],
            )

