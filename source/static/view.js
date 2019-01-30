/**
 * view.js
 * @author: Marko Čibej
 * @description: all the views, for the time being
*/


/**
 * The cards view
 */
var writing = (function writing(self, $) {
  'use strict';

  // card deck
  self.CardsView = function(deck) {
    let _this = this;

    // locate and save the templates for DOM elements we use
    this.deck = deck;
    this.card_template = $(this.deck.find('#card-template').html());
    this.sep2_template = $(this.deck.find('#card-sep-2').html());
    this.sep3_template = $(this.deck.find('#card-sep-3').html());
    this.sep4_template = $(this.deck.find('#card-sep-4').html());
    this.sep5_template = $(this.deck.find('#card-sep-5').html());

    // user events that we handle
    $('#reload-file').click(function() {
      _this.adapter.import();
    });

    // publicise the events we trigger
    this.onAdd = new self.Event(this);
    this.onUpdate = new self.Event(this);
    this.onDelete = new self.Event(this);

    // initialize the adapter and attach to it
    this.adapter = new self.Works();
    this.adapter.attachView(this);
    // wire up the events we are interested in
    if (this.adapter.hasOwnProperty('onReload')) {
      this.adapter.onReload.attach( (sender, data) => this.redisplay() ) };

    // finally, start the initial reload
    this.adapter.reload();
  };

  self.CardsView.prototype = {
    redisplay() {
      let works = this.adapter.getWorks();
      let prompt_ids = ['world-prompt',
                        'series-prompt',
                        'genre-prompt',
                        'form-prompt',
                        'status-prompt',
                        'count-prompt'];

      let prompt_values = this.adapter.translateList('ui', prompt_ids);

      for (let i = 0; i < prompt_ids.length; ++i) {
        this.card_template.find('#' + prompt_ids[i]).html(prompt_values[i]);
      }

      this.deck.empty();

      for (let [row, work] of works.entries()) {
        let newCard = this.card_template.clone();
        newCard.find('#work-title').html(work.name);
        if (work.name.length > 50) {
          newCard.find('#work-title').addClass('reduced'); //.css("font-size","70%");
        }
        else if (work.name.length > 35) {
          newCard.find('#work-title').addClass('small'); //.css("font-size","80%");
        }

        newCard.find('#count-top').html(work.word_count);
        newCard.find('#world').html(work.world);
        newCard.find('#series').html(work.series);
        newCard.find('#genre').html(work.genre);
        newCard.find('#form').html(work.form);
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
})(writing || {}, jQuery);
