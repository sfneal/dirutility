import PySimpleGUI as gui
from dirutility import desktop


def _line(char='_', width=100, size=(70, 1)):
    return gui.Text(char * width, size=size)


class WalkGUI:
    def __init__(self):
        """GUI window for inputing DirPaths parameters"""
        self.title = 'DirPaths'
        self.params = {}

    def __iter__(self):
        return iter(self.params)

    def __str__(self):
        return str(self.params)

    def _saving(self):
        """Parameters for saving results to file"""
        with gui.FlexForm(self.title, auto_size_text=True, default_element_size=(40, 1)) as form:
            layout = [
                [gui.Text('Results Saving Settings', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                # Source
                [gui.Text('Destination Folder', size=(15, 1), auto_size_text=False), gui.InputText(desktop()),
                 gui.FolderBrowse()],

                # File types
                [gui.Text('Select file types you would like to save output to.')],
                [gui.Checkbox('CSV', default=True), gui.Checkbox('JSON')],
                [_line()],

                # Save results to file
                [gui.Submit(), gui.Cancel()]]

            (button, (values)) = form.LayoutAndShow(layout)

        # gui.MsgBox(self.title, 'Parameters set', 'The results of the form are... ',
        #            'The button clicked was "{}"'.format(button), 'The values are', values, auto_close=True)

        self.params['save'] = {
            'directory': values[0],
            'csv': values[1],
            'json': values[2],
        }
        return self.params

    def parsing(self):
        """Parameters for parsing directory trees"""
        with gui.FlexForm(self.title, auto_size_text=True, default_element_size=(40, 1)) as form:
            layout = [
                [gui.Text('Directory Paths utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                # Source
                [gui.Text('Source Folder', size=(15, 1), auto_size_text=False), gui.InputText('Source'),
                 gui.FolderBrowse()],

                # Parallel / Sequential
                [gui.Text('Parallel or Sequential Processing. Larger directory trees are typically parsed faster '
                          'using parallel processing.')],
                [gui.Radio('Parallel Processing', "RADIO1"), gui.Radio('Sequential Processing', "RADIO1",
                                                                       default=True)],
                [_line()],

                # Files and non-empty-folders
                [gui.Text('Return files or folders, returning folders is useful for creating inventories.')],
                [gui.Radio('Return Files', "RADIO2", default=True), gui.Radio('Return Non-Empty Directories',
                                                                              "RADIO2")],
                [_line()],

                # max_level
                [gui.Text('Max Depth.... Max number of sub directory depths to traverse (starting directory is 0)')],
                [gui.InputCombo(list(reversed(range(0, 13))), size=(20, 3))],
                [_line()],

                # Relative and absolute
                [gui.Text('Relative or Absolute Paths.  Relative paths are saved relative to the starting directory. '
                          'Absolute paths are saved as full paths.')],
                [gui.Radio('Relative Paths', "RADIO3", default=True), gui.Radio('Absolute Paths', "RADIO3")],
                [_line()],

                # Topdown and output
                [gui.Checkbox('Topdown Parse', default=True), gui.Checkbox('Live output results')],
                [_line()],

                # Save results to file
                [gui.Checkbox('Save Results to File', default=False)],
                [gui.Submit(), gui.Cancel()]]

            (button, (values)) = form.LayoutAndShow(layout)

        # gui.MsgBox(self.title, 'Parameters set', 'The results of the form are... ',
        #            'The button clicked was "{}"'.format(button), 'The values are', values, auto_close=True)

        self.params['parse'] = {
            'directory': values[0],
            'parallelize': values[1],
            'sequential': values[2],
            'yield_files': values[3],
            'non_empty_folders': values[4],
            'max_level': int(values[5]),
            '_relative': values[6],
            'full_paths': values[7],
            'topdown': values[8],
            'console_stream': values[9],
            'save_file': values[10],
        }

        if self.params['parse']['save_file']:
            self._saving()

        return self.params


class BackupZipGUI:
    def __init__(self):
        """GUI window for saving zip backups"""
        self.title = 'ZipBackup'

    @property
    def source(self):
        """Parameters for saving zip backups"""
        with gui.FlexForm(self.title, auto_size_text=True, default_element_size=(40, 1)) as form:
            layout = [
                [gui.Text('Zip Backup utility', size=(30, 1), font=("Helvetica", 30), text_color='blue')],
                [gui.Text('Create a zip backup of a file or directory.', size=(50, 1), font=("Helvetica", 18),
                          text_color='black')],
                [gui.Text('-' * 200)],

                # Source
                [gui.Text('Select source folder', size=(20, 1), font=("Helvetica", 25), auto_size_text=False),
                 gui.InputText('', key='source', font=("Helvetica", 20)),
                 gui.FolderBrowse()],

                [gui.Submit(), gui.Cancel()]]

            button, values = form.LayoutAndRead(layout)
            if button == 'Submit':
                return values['source']
            else:
                exit()


class CompareTreesGUI:
    def __init__(self):
        self.title = 'CompareTrees'
        self.params = {}

    def _saving(self):
        with gui.FlexForm(self.title, auto_size_text=True, default_element_size=(40, 1)) as form:
            layout = [
                [gui.Text('Results Saving Settings', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                # Source
                [gui.Text('Destination Folder', size=(15, 1), auto_size_text=False), gui.InputText(desktop()),
                 gui.FolderBrowse()],

                # File types
                [gui.Text('Select file types you would like to save output to.')],
                [gui.Checkbox('CSV', default=True), gui.Checkbox('JSON')],
                [_line()],

                # Save results to file
                [gui.Submit(), gui.Cancel()]]

            (button, (values)) = form.LayoutAndShow(layout)

        self.params['save'] = {
            'directory': values[0],
            'csv': values[1],
            'json': values[2],
        }
        return self.params

    @property
    def sources(self):
        with gui.FlexForm(self.title, auto_size_text=True, default_element_size=(40, 1)) as form:
            layout = [
                [gui.Text('Compare Trees utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],

                # Source 1
                [gui.Text('Select source #1 folder', size=(15, 1), auto_size_text=False),
                 gui.InputText('Source'),
                 gui.FolderBrowse()],

                # Source 2
                [gui.Text('Select source #2 folder', size=(15, 1), auto_size_text=False),
                 gui.InputText('Source'),
                 gui.FolderBrowse()],

                # Save results to file
                [gui.Checkbox('Save Results to File', default=False)],

                [gui.Submit(), gui.Cancel()]]

            (button, (values)) = form.LayoutAndShow(layout)

        print(values)
        self.params['source'] = {
            'dir1': values[0],
            'dir2': values[1],
            'save_file': values[2],
        }

        if self.params['source']['save_file']:
            self._saving()
        return self.params
