from sklearn.metrics import roc_auc_score
from keras.callbacks import Callback


class RocAucEvaluation(Callback):
    """Calculate Roc AUC score and save the model after every epoch base on the score
    `filepath` can contain named formatting options,
    which will be filled the value of `epoch` and
    keys in `logs` (passed in `on_epoch_end`).
    For example: if `filepath` is `weights.{epoch:02d}-{val_loss:.2f}.hdf5`,
    then the model checkpoints will be saved with the epoch number and
    the validation loss in the filename.
    # Arguments
        filepath: string, path to save the model file.
        monitor: quantity to monitor.
        verbose: verbosity mode, 0 or 1.
        save_best_only: if `save_best_only=True`,
            the latest best model according to
            the quantity monitored will not be overwritten.
        save_weights_only: if True, then only the model's weights will be
            saved (`model.save_weights(filepath)`), else the full model
            is saved (`model.save(filepath)`).
        period: Interval (number of epochs) between checkpoints.
        validation_data: validattion X, Y (because ROC AUC can be calculated only in the end of epoch).
    """

    def __init__(self, filepath, validation_data=(), interval=1, save_weights_only=True):
        super(Callback, self).__init__()

        self.filepath = filepath
        self.best_score = 0.0
        self.interval = interval
        self.X_val, self.y_val = validation_data
        self.save_weights_only = save_weights_only

    def on_epoch_end(self, epoch, logs={}):
        if epoch % self.interval == 0:
            y_pred = self.model.predict(self.X_val, verbose=0)
            score = roc_auc_score(self.y_val, y_pred)
            print("\n ROC-AUC - epoch: %d - score: %.6f \n" % (epoch + 1, score))

            if self.best_score:
                self.best_score = score
                path = self.filepath.format(epoch=epoch, val_acc=score)
                print('save model to ', path)
                self.model.save(path)

            elif self.best_score < score:
                self.best_score = score
                path = self.filepath.format(epoch=epoch, val_acc=score)
                print('save model to ', path)
                self.model.save(path)