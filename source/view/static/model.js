/**
 * model.js
 * @author: Marko Čibej
 * @description: the model, inspired by simpleMVC by Todd Zebert
 * https://medium.com/@ToddZebert/a-walk-through-of-a-simple-javascript-mvc-implementation-c188a69138dc.
 */


/**
 * The model encapsulates the following:
 * Server represents the server connection and the sum of all the data. It implements the following:
 *   reload - clears everything and retrieves a fresh version of the data
 *   onReload - event that is triggered after a reload
 *   setLanguage
 * Works is a list of all works, versions and parts. It implements:
 *   getWorks - get a list of works, potentially with all parts, potentially with full histories
 *   addWork - add a new work
 *   addVersion - add a version to a work
 *   addPart - add a part or a file to a work or a part
 *   modify* - change the time-independent attributes of a work, version or part
 *   update* - update the history of a time dependent attribute
 */
var mvc = (function mvc(self, $) {
  'use strict';

  self.Works = function WorksModel() {
    this.works = {};
    this.onReload = new self.Event(this);
    this.onAdd = new self.Event(this);
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
      request.open("GET", "/all", true);
      request.send();
    },

    // get the simple version of the works list
    getWorks() {
      let work_list = [];
      for (let [n, w] of this.works.works.entries()) {
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
      this.onAdd.notify({ data: work });
    },
  };

  return self;
})(mvc || {}, jQuery);


