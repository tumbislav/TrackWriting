/**
 * model.js
 * @author: Marko Čibej
 * @description: the model, inspired by simpleMVC by Todd Zebert
 * https://medium.com/@ToddZebert/a-walk-through-of-a-simple-javascript-mvc-implementation-c188a69138dc.
*/


var mvc = (function mvc(self, $) {
  'use strict';

  self.Works = function WorksModel() {
    this.works = {};  // don't initialize, get it from the server

    this.onAdd = new self.Event(this);
  };

  // define getters and setters
  self.Works.prototype = {

    // get the simple version of the works list
    getWorks() {
      return this.data;
    },

    // add a work and notify listeners
    addWork(work) {
      this.data.append(work);  //TODO this ain't python
      this.onAdd.notify({ data: work });
    },
  };

  return self;
})(mvc || {}, jQuery);


