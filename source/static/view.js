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
    self.CardsView = function (deck) {
        let _this = this;

        // locate and save the templates for DOM elements we use
        this.deck = deck;
        this.card_template = $(this.deck.find('#card-template').html());
        this.sep2_template = $(this.deck.find('#card-sep-2').html());
        this.sep3_template = $(this.deck.find('#card-sep-3').html());
        this.sep4_template = $(this.deck.find('#card-sep-4').html());
        this.sep5_template = $(this.deck.find('#card-sep-5').html());

        // user events that we handle
        $('#mnu-reimport').click(function () {
            _this.adapter.import();
        });

        deck.on('keydown', '.tw-count', function (e) {
            let keycode = e.charCode || e.keyCode;
            if (keycode == 13) {
                let card = $(e.target).closest('.card');
                let new_data = card.data('json');
                new_data.word_count = Number($(e.target).html());
                _this.onUpdate.notify(new_data);
                return false;
            }
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
            this.adapter.onReload.attach((sender, data) => this.redisplay())
        };

        if (this.adapter.hasOwnProperty('onError')) {
            this.adapter.onReload.attach((sender, data) => console.write(data))
        };

        // finally, start the initial reload
        this.adapter.reload();
    };

    self.CardsView.prototype = {
        translateUI() {
        },
        redisplay() {
            let works = this.adapter.getWorks();
            let prompt_ids = ['tw-tag-world',
                'tw-tag-series',
                'tw-tag-genre',
                'tw-tag-form',
                'tw-tag-status',
                'tw-tag-count',
                'tw-mnu-reimport'];

            let prompt_values = this.adapter.translateList('ui-card', prompt_ids);

            for (let i = 0; i < prompt_ids.length; ++i) {
                this.card_template.find('.' + prompt_ids[i]).html(prompt_values[i]);
            }

            this.deck.empty();

            for (let[row, work]of works.entries()) {
                let newCard = this.card_template.clone();
                let nameDiv = newCard.find('.tw-name');
                nameDiv.html(work.name);
                if (work.name.length > 50) {
                    nameDiv.addClass('reduced');
                } else if (work.name.length > 35) {
                    nameDiv.addClass('small');
                }

                newCard.find('.tw-world').html(work.world);
                newCard.find('.tw-series').html(work.series);
                newCard.find('.tw-genre').html(work.genre);
                newCard.find('.tw-form').html(work.form);
                newCard.find('.tw-status').html(work.status);
                newCard.find('.tw-count').html(work.word_count);
                newCard.data('json', work);
                this.deck.append(newCard);

                if (row % 2 == 1) {
                    this.deck.append(this.sep2_template.clone());
                }
                if (row % 3 == 2) {
                    this.deck.append(this.sep3_template.clone());
                }
                if (row % 4 == 3) {
                    this.deck.append(this.sep4_template.clone());
                }
                if (row % 5 == 4) {
                    this.deck.append(this.sep5_template.clone());
                }
            }
        },
    };

    return self;
})(writing || {}, jQuery);