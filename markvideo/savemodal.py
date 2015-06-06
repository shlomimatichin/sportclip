from Tkinter import *
import json
import os


class SaveModal:
    def __init__(self, jsonsDir, data):
        self._jsonsDir = jsonsDir
        self._data = data
        self._prefix = data['clipType']
        self.top = Tk()
        self.top.grid()
        label = Label(self.top, text="Description: ")
        label.grid(column=0, row=0, sticky="EW")
        label = Label(self.top, text="Caption: ")
        label.grid(column=0, row=1, sticky="EW")
        self.entry1 = Entry(self.top, bd=5)
        self.entry1.grid(column=1, row=0, sticky="EW")
        self.entry1.bind("<Return>", self._next)
        self.entry1.bind("<Escape>", self._abort)
        self.entry2 = Entry(self.top, bd=5)
        self.entry2.grid(column=1, row=1, sticky="EW")
        self.entry2.bind("<Return>", self._done)
        self.entry2.bind("<Escape>", self._abort)

    def run(self):
        self.top.mainloop()

    def _abort(self, *args):
        print "Aborted with ESC"
        self.top.quit()

    def _next(self, *args):
        self.entry2.focus_set()

    def _done(self, *args):
        if self.entry1.get() == "":
            print "Will not save empty description"
            self.top.quit()
            return
        self._data['description'] = self.entry1.get()
        self._data['caption'] = self.entry2.get()
        for i in xrange(100000):
            fullName = os.path.join(
                self._jsonsDir, "%s_%05d.json" % (self._prefix, i))
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
