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
    this.translations = null;
    // the configuration
    this.preferred_language = 'en';

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
        }),
        $.get('/translations', function(response){
          _this.translations = JSON.parse(response);
        })
      ).then(function(){
        _this.onReload.notify();
      })
    },

    translateString(translation, context, value) {
      if (translation.hasOwnProperty(context) && translation[context].hasOwnProperty(value)) {
        return translation[context][value];
      }
      else {
        return value;
      }
    },

    translateWork(work) {
      let translations = {};
      let adapted = {};
      if (this.preferred_language != null && this.translations.hasOwnProperty(this.preferred_language)) {
        translations = this.translations[this.preferred_language];
      }
      adapted.id = work.id;
      adapted.name = work.name;
      adapted.world = work.world;
      adapted.series = work.series;
      adapted.genre = this.translateString(translations, 'genres', work.genre);
      adapted.type = work.type;
      adapted.status = work.status;
      adapted.word_count = work.word_count;
      return adapted;
    },

    // get the simple version of the works list
    getWorks() {
      let work_list = [];
      for (let [n, work] of this.works.entries()) {
        work_list.push(this.translateWork(work));
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


