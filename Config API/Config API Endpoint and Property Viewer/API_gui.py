# *****************************************************************************
#  * 
#  * This file is copyright (c) PTC, Inc.
#  * All rights reserved.
#  * 
#  * Name:        API_gui.py
#  * Description: A simple GUI app that provides a visualization of the Kepware
#  *    Configuration API.
#  * 
#  * 
#  * Update History:
#  * 0.0.1:     Initial Release
#  * 0.0.2:     Allowed UA Gateway to be processed
#  *            Prevent Plug-in root branches from being created if not installed
#  *                on server
#  * 0.0.3:     Added Search Feature - Search in text box for api data
#  *            Provided a Methods output in text to associate type definition  
#  *                access properties to HTTP Methods
#  * 0.0.4:     Added Doc Endpoint Information to text box to provide user additional
#  *            information
#  * 
#  * Version:     0.0.4
# ******************************************************************************

from tkinter import *
from tkinter import ttk, messagebox

import json
import re
from widgets import searchbar, treevscroll, textscroll
from server import server_doc

COLUMNS = ['doc_path', 'endpoint', 'parent_endpoint']

class App(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       

        # Kepware Connection config
        self.server = server_doc(None, None, None, None)
        self.api_root = None

        self.grid(column=0, row=0, sticky=NSEW)
        self.columnconfigure(0, weight=1, uniform='test')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=10)

        # Access Frame with credentials and host information
        self.accessframe = ttk.Frame(self)
        self.accessframe.grid(column=0, row=0, sticky=NSEW)

        self.serverframe = ttk.Labelframe(self.accessframe, text='Kepware Server Address', padding="3 3 12 12")
        self.serverframe.grid(column=0, row=0, sticky=NSEW)

        self.hostVar = StringVar()
        self.hostVar.set('localhost')
        self.hostEntry = ttk.Entry(self.serverframe, textvariable=self.hostVar)
        self.hostEntry.grid(column=1, row=0, sticky=NSEW)
        Label(self.serverframe, text='Host/IP:').grid(column=0, row=0, sticky=E)

        self.portVar = StringVar()
        self.portVar.set('57512')
        self.portEntry = ttk.Entry(self.serverframe, textvariable=self.portVar)
        self.portEntry.grid(column=1, row=1, sticky=NSEW)
        Label(self.serverframe, text='Port:').grid(column=0, row=1, sticky=E)

        self.__optionList = ['https', 'http']
        self.httpVar = StringVar()
        self.httpSelect = ttk.OptionMenu(self.serverframe, self.httpVar, self.__optionList[0], *self.__optionList, command= self.httpSelectEvent)
        self.httpSelect.grid(column=1, row=2, sticky=NW)
        self.httpSelect.configure()

        self.trustCertsVar = BooleanVar()
        self.trustCertsSelect = ttk.Checkbutton(self.serverframe, variable=self.trustCertsVar, text='Trust All Certs?')
        self.trustCertsSelect.grid(column=1, row=3, sticky=NW)


        self.credframe = ttk.Labelframe(self.accessframe, text='Authorization', padding="3 3 12 12")
        self.credframe.grid(column=1, row=0, sticky=NSEW)

        self.userVar = StringVar()
        self.userVar.set('Administrator')
        self.userEntry = ttk.Entry(self.credframe, textvariable=self.userVar)
        self.userEntry.grid(column=1, row=0, sticky=NSEW)
        Label(self.credframe, text='Username:').grid(column=0, row=0, sticky=E)

        self.passVar = StringVar()
        self.passVar.set('')
        self.passEntry = ttk.Entry(self.credframe, textvariable=self.passVar)
        self.passEntry.grid(column=1, row=1, sticky=NSEW)
        Label(self.credframe, text='Password:').grid(column=0, row=1, sticky=E)

        self.btnFrame = ttk.Frame(self.accessframe)
        self.btnFrame.grid(column=3, row=0, sticky=NSEW)
        self.connectBtn = ttk.Button(self.btnFrame, text='Connect', command=self.connect)
        self.connectBtn.grid(column=0, row=0, sticky=W)
        self.disconnectBtn = ttk.Button(self.btnFrame, text='Disconnect', command=self.disconnect, state=DISABLED)
        self.disconnectBtn.grid(column=0, row=1, sticky=W)

        # Search Bar
        self.searchPos = {'idx': '1.0'}
        self.searchBar = searchbar(self, column=0, row=1, command= self.search)

        # Frame to Visualize tree and doc text
        self.dataframe = PanedWindow(self, orient=HORIZONTAL, sashpad='2p', sashwidth='4p', sashrelief='sunken', showhandle=TRUE)
        self.dataframe.grid(column=0, row=2, sticky=NSEW)
        self.dataframe.rowconfigure(0, weight=1)

        # Tree Browser Object
        self.treeframe = treevscroll(self.dataframe, row=0, columns=COLUMNS)
        self.dataframe.add(self.treeframe)
        self.event_add('<<tree_select>>', '<Double-1>', '<Return>')
        self.treeframe.treev.tag_bind('item', '<<tree_select>>', self.item_click)
        self.treeframe.treev.tag_bind('root', '<<tree_select>>', self.root_click)

        # Text Frame Object for Output of Documentation
        self.textframe = textscroll(self.dataframe, row=0)
        self.dataframe.add(self.textframe)
        self.textframe.text.config(state=DISABLED)
        self.textframe.text.tag_config('endpoint', foreground='blue')
        self.textframe.text.tag_config('methods')
        self.textframe.text.tag_config('url', underline=1)

    # Event for selecting Connect button
    def connect(self):
        http = False
        if self.httpVar.get() == 'https':
            http = True
        self.server = server_doc(self.hostVar.get(), self.portVar.get(), self.userVar.get(), self.passVar.get(), http)
        self.server.SSL_trust_all_certs = self.trustCertsVar.get()
        try:
            self.api_root = self.server.get_doc('/config/v1/doc')
        except Exception as err:
            self.server.ErrorHandler(err)
        else:
            self.build_tree_root(self.api_root)
            self.connectBtn.state(('disabled',))
            self.disconnectBtn.state(('!disabled',))
            self.hostEntry.configure(state=DISABLED)
            self.portEntry.configure(state=DISABLED)
            self.userEntry.configure(state=DISABLED)
            self.passEntry.configure(state=DISABLED)
            self.httpSelect.configure(state=DISABLED)

    # Event for selecting Disconnect button
    def disconnect(self):
        root_iids = self.treeframe.treev.get_children()
        [self.treeframe.treev.delete(branch) for branch in root_iids]
        self.update_text_window('')
        self.connectBtn.state(('!disabled',))
        self.disconnectBtn.state(('disabled',))
        self.httpSelect.configure(state=NORMAL)
        self.hostEntry.configure(state=NORMAL)
        self.portEntry.configure(state=NORMAL)
        self.userEntry.configure(state=NORMAL)
        self.passEntry.configure(state=NORMAL)
    
    # Event for searching
    #function to search string in text
    def search(self, *args):
        
        #remove tag 'found' from index 1 to END
        self.textframe.text.tag_remove('found', '1.0', END)
        
        #returns to widget currently in focus
        s = self.searchBar.input.get()
        if not s:
            return
        idx = self.searchPos['idx']
        
        #searches for desired string from index 1
        idx = self.textframe.text.search(s, idx, nocase=1,)
        if not idx: 
            self.searchPos['idx'] = '1.0'
            messagebox.showinfo('Not Found', f'"{s}" not found.')
            return 
        
        #last index sum of current index and
        #length of text
        lastidx = '%s+%dc' % (idx, len(s))
        
        #overwrite 'Found' at idx
        self.textframe.text.tag_add('found', idx, lastidx)
        self.searchPos['idx'] = lastidx
        self.textframe.text.see(idx)
        
        #mark located string as red
        self.textframe.text.tag_config('found', background='#3282F6', foreground='white')
        self.searchBar.input.focus_set()
    
    # Event for selecting protocol
    def httpSelectEvent(self, event):
        if event == 'http':
            self.trustCertsSelect.configure(state=DISABLED)
        else:
            self.trustCertsSelect.configure(state=NORMAL)
           
    # Event for Root branches
    def root_click(self, event: Event):
        item = event.widget.selection()
        info = event.widget.item(item[0])
        r = self.server.get_doc(info['values'][COLUMNS.index('doc_path')])
        self.update_text_window(r, info['values'][COLUMNS.index('endpoint')], info['values'][COLUMNS.index('doc_path')])
    
    # Event for other branches
    def item_click(self, event: Event):
        item = event.widget.selection()
        info = event.widget.item(item[0])
        r = self.server.get_doc(info['values'][COLUMNS.index('doc_path')])
        self.update_text_window(r, info['values'][COLUMNS.index('endpoint')], info['values'][COLUMNS.index('doc_path')])
        if info['text'] in ['tag_groups', 'tags']:
            return

        if 'child_collections' in r['type_definition']:
            [self.child_collection_insert(item[0], j) for j in r['type_definition']['child_collections']]
    
    # Init Driver tree branch
    def driver_tree_insert(self, root, driver):
        branch = self.treeframe.treev.insert(root, END, text=driver['display_name'], tags='driver')
        
        # Search doc keys
        children = []
        efm_children = []
        for j in driver.keys():
            if j.startswith('doc') and j.find('doc_meters') == -1 and j.find('doc_meter_groups') == -1:
                name = j[4:]
                urls = [child for child in self.api_root if re.search(rf'/{name}$', child['endpoint'])]
                children.append([j,name, urls[0]])
            # elif j.find('doc_meters') != -1 or j.find('doc_meter_groups') != -1:
            elif j.find('doc_meter_groups') != -1:
                name = j[4:]
                urls = [child for child in self.api_root if re.search(rf'/{name}$', child['endpoint'])]
                efm_children.append([j,name, urls[0]])
        [self.treeframe.treev.insert(branch,END, text=name, tags='item', values=[driver[doc], url['endpoint']]) for doc, name, url in children]
        if efm_children:
            root_iids = self.treeframe.treev.get_children(branch)
            for iid in root_iids:
                childname = self.treeframe.treev.item(iid, option='text')
                if childname == 'devices':
                    [self.treeframe.treev.insert(iid,END, text=name, tags='item', values=[driver[doc], url['endpoint']]) for doc, name, url in efm_children]
            pass

    
    # Init Plug-In tree branch
    def plug_in_collection_insert(self, root, collection: str):
        exist_children = [self.treeframe.treev.item(children)['text'] for children in self.treeframe.treev.get_children(root)]
        if collection.startswith('_') and collection not in exist_children:
            parent_endpoint = f'/config/v1/project/'
            # Find Children in API doc list
            filtered = [child for child in self.api_root if re.search(rf'/{collection}/(\w+)$', child['endpoint'])]
            # Filtered will return API endpoints for Plug-ins if it is installed. If the plug-in isn't installed, don't 
            # create branch.
            if filtered:
                branch = self.treeframe.treev.insert(root, END, text=collection, values=['',f'{parent_endpoint}/{collection}',])
                for item in filtered:
                    self.treeframe.treev.insert(branch, END, text=re.search(rf'/{collection}/(\w+)$', item['endpoint']).groups()[0], tags='item', values=[item['doc'], item['endpoint'], parent_endpoint])

    # Init All Endpoints tree
    def build_end_point_tree(self, root, endpoint_list, startpoint='/config/v1'):
        # Build Parents list at startpoint
        parents = []
        for i in endpoint_list:
            matches = re.search(startpoint + r'\/([{]*[\w]*[}]*\?\S*|[{]*[\w]*[}]*)\/?\S*', i['endpoint'])
            if matches:
                parents.append(matches.groups()[0])
        parents = list(set(parents))
        parents.sort()
        for p in parents:
            p_url = f'{startpoint}/{p}'
            p_endpoint = [epdict for epdict in self.api_root if epdict['endpoint']== p_url]
            c_endpoints = [epdict for epdict in self.api_root if epdict['endpoint'].find(p_url) != -1]
            branch = None
            if 'doc' in p_endpoint[0]:
                branch = self.treeframe.treev.insert(root, END, text= p_url, tags='root', values=[p_endpoint[0]['doc'], p_url])
            else:
                branch = self.treeframe.treev.insert(root, END, text= p_url, tags='names')
            self.build_end_point_tree(branch, c_endpoints, p_url)

    # Init Tree after connections 
    def build_tree_root(self, info):
        root_list = [('Drivers', '/config/v1/doc/drivers', '/config/v1/doc/drivers', 'root'), ('Project','/config/v1/doc/project', '/config/v1/project', 'root'), ('Plug-ins','/config/v1/doc/project', '', 'root'),
                    ('Admin','/config/v1/doc/admin', '/config/v1/admin', 'root'), ('All Endpoints','/config/v1/doc', '/config/v1/doc', 'root')]
        [self.treeframe.treev.insert('',END, text=i, open=False, tags=l, values=[j, k]) for i,j,k,l in root_list]

        root_iids = self.treeframe.treev.get_children()

        for i, (name, path, url, tag) in enumerate(root_list):
            r = self.server.get_doc(path)
            if name == 'Drivers':
                tree_items = sorted(r, key=lambda d: d['display_name'])
                [self.driver_tree_insert(root_iids[i], driver) for driver in tree_items]
            elif name in ['Project', 'Admin']:
                if r['type_definition']['child_collections']:
                    tree_items = sorted(r['type_definition']['child_collections'])
                    [self.child_collection_insert(root_iids[i], j) for j in tree_items]
            elif name == 'Plug-ins':
                if r['type_definition']['child_collections']:
                    tree_items = sorted(r['type_definition']['child_collections'])
                    [self.plug_in_collection_insert(root_iids[i], j) for j in tree_items]
            elif name == 'All Endpoints':
                tree_items = sorted(r, key=lambda d: d['endpoint'])
                self.build_end_point_tree(root_iids[i], tree_items)
            else:
                pass

    # Build Children tree branchs
    def child_collection_insert(self, root, collection):
        exist_children = [self.treeframe.treev.item(children)['text'] for children in self.treeframe.treev.get_children(root)]
        if collection not in ['devices', 'channels', 'meter_groups'] + exist_children and not collection.startswith('_'):
            # Find Collection in API doc list relative to parent path
            parent_endpoint= self.treeframe.treev.item(root)['values'][COLUMNS.index('endpoint')]
            if parent_endpoint in ['/config/v1/project', '/config/v1/admin']:
                col = [coldict for coldict in [cdict for cdict in self.api_root if 'doc' in cdict] if coldict['doc'].find(collection) != -1 and re.search(f'{parent_endpoint}/{collection}', coldict['endpoint'])]
            else:
                col = [coldict for coldict in [cdict for cdict in self.api_root if 'doc' in cdict] if coldict['doc'].find(collection) != -1 and re.search(parent_endpoint + r'\/\{\w+\}\/' + collection, coldict['endpoint'])]
            # Make sure a match is found
            if col:
                self.treeframe.treev.insert(root, END, text=collection, tags='item', values=[col[0]['doc'],col[0]['endpoint'], parent_endpoint])

    def processMethods(self, DATA):
        methods = {'GET': True, 'DELETE': False, 'POST': False, 'PUT': False}
        if 'type_definition' in DATA:
            if DATA['type_definition']['can_create']:
                methods['POST'] = True
            if DATA['type_definition']['can_delete']:
                methods['DELETE'] = True
            if DATA['type_definition']['can_modify']:
                methods['PUT'] = True
        return methods

    # Update text window with data to present to user
    def update_text_window(self, DATA = None, endpoint = '', docEndpoint = ''):
        if endpoint != '':
            methods = self.processMethods(DATA)
            self.textframe.update([(f'ENDPOINT:\n', ('header','endpoint')), 
                                   (f'{endpoint}\n\n',('endpoint', 'url')),
                                   (f'DOC ENDPOINT:\n', ('header', 'endpoint')),
                                   (f'{docEndpoint}\n\n',('endpoint', 'url')),
                                   (f'METHODS:\n{json.dumps(methods, indent=2)}\n\n', 'methods'),
                                   (f'DOCUMENTATION:\n{json.dumps(DATA, indent=2)}','doc')])
        elif DATA:
            methods = self.processMethods(DATA)
            self.textframe.update([(f'METHODS:\n{json.dumps(methods, indent=2)}\n\n', 'methods'), (f'DOCUMENTATION:\n{json.dumps(DATA, indent=2)}','doc')])
        else:
            self.textframe.clear()




if __name__ == "__main__":
    root = Tk()
    root.title("Kepware Server API Documentation Viewer")
    root.minsize(width=500, height=200)
    root.columnconfigure(0, minsize=200, weight=1)
    root.rowconfigure(0, weight=1)
    sizegrip = ttk.Sizegrip(root)
    sizegrip.grid(row=1, sticky=SE)

    mainframe = App(root, padding="3 3 12 12")

    root.mainloop()