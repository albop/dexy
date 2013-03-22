from dexy.reporter import Reporter
import os

class OutputReporter(Reporter):
    """
    Creates canonical dexy output with files given short filenames.
    """
    aliases = ['output']
    _settings = {
            'dir' : 'output'
            }

    def write_canonical_doc(self, data):
        fp = os.path.join(self.setting('dir'), data.name)

        if fp in self.locations:
            print "WARNING overwriting file", fp
        else:
            self.locations[fp] = []
        self.locations[fp].append(data.key)

        parent_dir = os.path.dirname(fp)
        try:
            os.makedirs(parent_dir)
        except os.error:
            pass

        self.log_debug("  writing %s to %s" % (data.key, fp))

        data.output_to_file(fp)

    def run(self, wrapper):
        self.wrapper=wrapper
        self.locations = {}

        self.create_reports_dir()
        for data in wrapper.batch:
            if data.is_canonical_output():
                self.write_canonical_doc(data)

class LongOutputReporter(Reporter):
    """
    Creates complete dexy output with files given long, unique filenames.
    """
    aliases = ['long']
    _settings = {
            'dir' : 'output-long'
            }

    def run(self, wrapper):
        self.wrapper=wrapper
        self.create_reports_dir()
        for doc in wrapper.batch:
            fp = os.path.join(self.setting('dir'), doc.long_name())

            try:
                os.makedirs(os.path.dirname(fp))
            except os.error:
                pass

            self.log_debug("  writing %s to %s" % (doc.key, fp))
            doc.output_to_file(fp)