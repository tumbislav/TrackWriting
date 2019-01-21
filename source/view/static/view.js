/**
 * view.js
 * @author: Marko Čibej
 * @description: a view, for the moment
 * inspired by simpleMVC by Todd Zebert
 * https://medium.com/@ToddZebert/a-walk-through-of-a-simple-javascript-mvc-implementation-c188a69138dc.
*/


/**
 * A 2-way View Module
 */
var mvc = (function mvc(self, $) {
  'use strict';

  // card deck
  self.Cards = function CardView(model, deck) {
    this.model = model;
    this.deck = deck;
    this.card_template = $(this.deck.find('#card-template').html());
    this.sep2_template = $(this.deck.find('#card-sep-2').html());
    this.sep3_template = $(this.deck.find('#card-sep-3').html());
    this.sep4_template = $(this.deck.find('#card-sep-4').html());
    this.sep5_template = $(this.deck.find('#card-sep-5').html());
  };

  self.Cards.prototype = {
    show() {
      let works = this.model.getWorks();
      for (let [row, work] of works.entries()) {
        let newCard = this.card_template.clone();
        newCard.find('#work-title').html(work.name);
        newCard.find('#count-top').html(work.word_count);
        newCard.find('#world').html(work.world);
        newCard.find('#series').html(work.series);
        newCard.find('#genre').html(work.genre);
        newCard.find('#type').html(work.type);
        newCard.find('#status').html(work.status);
        newCard.find('#count').html(work.word_count);
        this.deck.append(newCard);

        if (row % 2 == 1) { this.deck.append(this.sep2_template.clone()); }
        if (row % 3 == 2) { this.deck.append(this.sep3_template.clone()); }
        if (row % 4 == 3) { this.deck.append(this.sep4_template.clone()); }
        if (row % 5 == 4) { this.deck.append(this.sep5_template.clone()); }
      }
    },
  };

  return self;
})(mvc || {}, jQuery);
