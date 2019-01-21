/**
 * controller.js
 * @author: Marko Čibej
 * @description: the controller module
 * inspired by simpleMVC by Todd Zebert
 * https://medium.com/@ToddZebert/a-walk-through-of-a-simple-javascript-mvc-implementation-c188a69138dc.
*/

var mvc = (function mvc(self, $) {
  'use strict';

  self.CardDealer = function CardController(model, view) {

    this.model = model;
    this.view = view;

    if (this.model.hasOwnProperty('onReload')) {
      this.model.onReload.attach(
        (sender, data) => this.dataReloaded()
      )
    }

    if (this.view.hasOwnProperty('onChanged')) {
      this.view.onChanged.attach(
        (sender, data) => this.update(data)
      );
    }
  };

  self.CardDealer.prototype = {
    update(data) {
      this.model.set(data);
    },
    dataReloaded() {
      this.view.show();
    },
  };

  return self;
})(mvc || {}, jQuery);
