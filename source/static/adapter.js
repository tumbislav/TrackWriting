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
var writing = (function writing(self, $) {
  'use strict';

  self.Works = function(view) {
    // the model's data cache
    this.works = null;
    this.classifiers = null;
    // the configuration
    this.preferred_language = 'default';

    // Events we generate ourselves.
    // initial load or reload
    this.onReload = new self.Event(this);
  };

  // the main functionality
  self.Works.prototype = {

    attachView(view) {
      // adding a new work
      if (view.hasOwnProperty('onAdd')) {
        view.onAdd.attach( (sender, data) => this.addWork(data) ) }
      // deleting a work
      if (view.hasOwnProperty('onDelete')) {
        view.onDelete.attach( (sender, data) => this.deleteWork(data) ) }
      // changing an existing work
      if (view.hasOwnProperty('onUpdate')) {
        view.onUpdate.attach( (sender, data) => this.updateWork(data) ) }
    },

    // clear current data and reload everything from server, then tell the views to refresh
    reload() {
      let _this = this;
      $.when(
        $.get('/works', function(response){
          _this.works = JSON.parse(response);
        }),
        $.get('/classifiers', function(response){
          _this.classifiers = JSON.parse(response);
        })
      ).then(function(){
        _this.onReload.notify();
      })
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
      $.noop();
    },
    deleteWork(work) {
      $.noop();
    },
  };

  return self;
})(writing || {}, jQuery);


