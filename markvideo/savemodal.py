from Tkinter import *
import json
import os


class SaveModal:
    def __init__(self, jsonsDir, data):
        self._jsonsDir = jsonsDir
        self._data = data
        self._prefix = data['clipType']
        self.top = Tk()
        self.label = Label(self.top, text="Description: ")
        self.label.pack(side = LEFT)
        self.entry = Entry(self.top, bd =5)
        self.entry.pack(side = RIGHT)
        self.entry.bind("<Return>", self._done)

    def run(self):
        self.top.mainloop()

    def _done(self, *args):
        if self.entry.get() == "":
            print "Will not save empty description"
            self.top.quit()
            return
        self._data['description'] = self.entry.get()
        for i in xrange(100000):
            fullName = os.path.join(
                self._jsonsDir, "%s_%d.json" % (self._prefix, i))
            if not os.path.exists(fullName):
                break
        with open(fullName, "w") as f:
            json.dump(self._data, f, indent=2)
        self.top.quit()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonsDir", required=True)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()
    data = json.loads(args.json)
    SaveModal(args.jsonsDir, data).run()
