

class SheltuzNotify(object):
    def __init__(self):
        self.success_code = "100.000.000"
        self.error_code = "900.000.000"
        self.failed_code = "900.000.001"
        self.not_found_code = "999.999.999"
        self.info_code = "302.000.000"

    def success(self):
        return self.success_code

    def failed(self):
        return self.failed_code

    def error(self):
        return self.error_code

    def not_found(self):
        return self.not_found_code

    def info(self):
        return self.info_code