/**
 * adapter.js
 * @author: Marko Čibej
 * @description: the adapter part of the application, responsible for communicating with the model
 *    that is defined by the REST API, and the controller that is model-agnostic.
 *    The application is enclosed in the 'writing' namespace.
 */



/**
 * The entire application is packaged in the 'writing' namespace.
 */
var writing = (function writing(self) {
  'use strict';

  self.Works = function(view) {
    // we start with an empty list of works
    this.works = [];
    // event to trigger on initial load or on reload
    this.onReload = new self.Event(this);

    this.view = view;

    // listen to the events we are interested in
    if (this.view.hasOwnProperty('onAdd')) {
      this.view.onAdd.attach( (sender, data) => this.addWork(data) ) }

    if (this.view.hasOwnProperty('onDelete')) {
      this.view.onReload.attach( (sender, data) => this.deleteWork(data) ) }

    if (this.view.hasOwnProperty('onUpdate')) {
      this.view.onReload.attach( (sender, data) => this.updateWork(data) ) }
  };

  // define getters and setters
  self.Works.prototype = {

    // clear all current data, if any, and reload it from the server
    reload() {
      this.works = null;
      let this_model = this;
      let request = new XMLHttpRequest();

      request.onreadystatechange = function() {
        if (this.readyState != 4 || this.status != 200) { return; }
        this_model.works = JSON.parse(this.responseText);
        this_model.onReload.notify();
      };
      request.open("GET", "/works", true);
      request.send();
    },

    // get the simple version of the works list
    getWorks() {
      let work_list = [];
      for (let [n, w] of this.works.entries()) {
        work_list.push({
          id: w.id,
          name: w.name,
          world: w.world,
          series: w.series,
          genre: w.genre,
          type: w.type,
          status: w.status,
          word_count: w.word_count
        });
      };
      return work_list;
    },

    // add a work and notify listeners
    addWork(work) {
      this.data.push(work);
    },
    deleteWork(work) {
      this.data.push(work);
    },
  };

  return self;
})(writing || {});


