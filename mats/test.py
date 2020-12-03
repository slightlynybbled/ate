import logging


class Test:
    """
    A test is the most basic unit of an executing test sequence.  Within
    a test, we may have a setup(), execute(), and teardown() method.  Only the
    `execute()` method is required to be overridden.

    :param moniker: a shortcut name for this particular test
    :param min_value: the minimum value that is to be considered a pass, \
    if defined
    :param max_value: the maximum value that is to be considered a pass, \
    if defined
    :param pass_if: the value that must be present in order to pass, if defined
    :param loglevel: the logging level to apply such as `logging.INFO`
    """

    def __init__(self, moniker, min_value=None, max_value=None, pass_if=None,
                 loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        if pass_if is not None:
            moniker_str = f'{moniker} (pass if={pass_if})'
        elif min_value is not None and max_value is not None:
            moniker_str = f'{moniker} (min={min_value:.3g}, max={max_value:.3g})'
        elif min_value is not None:
            moniker_str = f'{moniker} (min={min_value:.3g})'
        elif max_value is not None:
            moniker_str = f'{moniker} (max={max_value:.3g})'
        else:
            moniker_str = moniker

        self.moniker = moniker_str
        self._max_value, self._min_value = max_value, min_value
        self._pass_if = pass_if

        self._test_is_passing = None
        self.value = None
        self.aborted = False
        self.status = 'waiting'

        self.saved_data = {}

    @property
    def is_passing(self):
        return self._test_is_passing

    def abort(self):
        self.aborted = True

    def _setup(self, is_passing):
        """
        Pre-execution method used for logging and housekeeping.

        :param is_passing: True if the test sequence is passing up to this \
        point, else False
        :return:
        """
        self._logger.info(f'setting up "{self.moniker}"')

        self._test_is_passing = True
        self.value = None
        self.status = 'running' if not self.aborted else 'aborted'

        self.aborted = False
        self.setup(is_passing=is_passing)
        self.status = 'running' if not self.aborted else 'aborted'

    def _execute(self, is_passing):
        """
        Pre-execution method used for logging and housekeeping.

        :param is_passing: True if the test sequence is passing up to this \
        point, else False
        :return:
        """
        self.status = 'running' if not self.aborted else 'aborted'
        if self.aborted:
            self._logger.warning('aborted, not executing')
            return

        self._logger.info(f'executing test "{self.moniker}"')

        self.value = self.execute(is_passing=is_passing)

        if self._pass_if is not None:
            if self.value != self._pass_if:
                self._logger.warning(
                    f'"{self.value}" != pass_if requirement '
                    f'"{self._pass_if}", failing')
                self.fail()
            else:
                self._logger.info(
                    f'"{self.value}" == pass_if requirement "{self._pass_if}"')

        if self._min_value is not None:
            if self.value < self._min_value:
                self._logger.warning(
                    f'"{self.value}" is below the minimum '
                    f'"{self._min_value}", failing')
                self.fail()
            else:
                self._logger.info(
                    f'"{self.value}" is above the minimum "{self._min_value}"')

        if self._max_value is not None:
            if self.value > self._max_value:
                self._logger.warning(
                    f'"{self.value}" is above the maximum "{self._max_value}"')
                self.fail()
            else:
                self._logger.info(
                    f'"{self.value}" is below the maximum "{self._max_value}"')

        self.status = 'running' if not self.aborted else 'aborted'

        return self.value

    def _teardown(self, is_passing):
        """
        Pre-execution method used for logging and housekeeping.

        :param is_passing: True if the test sequence is passing up to \
        this point, else False
        :return:
        """
        if self.aborted:
            self.status = 'aborted'
            self._logger.warning('aborted, not executing')
            return

        self._logger.info(f'tearing down "{self.moniker}"')

        self.teardown(is_passing)
        self.status = 'complete'

    def reset(self):
        """
        Reset the test status
        :return: None
        """
        self.status = 'waiting'

    def save_dict(self, data: dict):
        """
        Allows a test to save additional data other than that returned \
        by ``execute()``

        :param data: key: value pairs of the data to be stored
        :return: None
        """
        self.saved_data = data.copy()

    def fail(self):
        """
        When called, will cause the test to fail.

        :return: None
        """
        self._test_is_passing = False

    def setup(self, is_passing):
        """
        Abstract method intended to be overridden by subclass

        :param is_passing: True if the test sequence is passing up to this \
        point, else False
        :return: None
        """
        pass

    def execute(self, is_passing):
        """
        Abstract method intended to be overridden by subclass

        :param is_passing: True if the test sequence is passing up to this \
        point, else False
        :return: value to be appended to the sequence dictionary
        """
        raise NotImplementedError

    def teardown(self, is_passing):
        """
        Abstract method intended to be overridden by subclass

        :param is_passing: True if the test sequence is passing up to this \
        point, else False
        :return: None
        """
        pass
