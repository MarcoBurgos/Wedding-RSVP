// Create Countdown
var Countdown = {

  // Backbone-like structure
  $el: $('.countdown'),

  // Params
  countdown_interval: null,
  total_seconds     : 0,

  // Initialize the countdown
  init: function() {

    // DOM
		this.$ = {
      days  : this.$el.find('.bloc-time.days .figure'),
    	hours  : this.$el.find('.bloc-time.hours .figure'),
    	minutes: this.$el.find('.bloc-time.min .figure'),
    	seconds: this.$el.find('.bloc-time.sec .figure')
   	};

    // Init countdown values
    this.values = {
        days  :  this.$.days.parent().attr('data-init-value'),
	      hours  : this.$.hours.parent().attr('data-init-value'),
        minutes: this.$.minutes.parent().attr('data-init-value'),
        seconds: this.$.seconds.parent().attr('data-init-value'),
    };




    // Initialize total seconds
    this.total_seconds = this.values.hours * 60 * 60 + (this.values.minutes * 60) + this.values.seconds;

    // Animate countdown to the end
    this.count();
  },

  count: function() {



    var that    = this,
        $days_1 = this.$.days.eq(0),
        $days_2 = this.$.days.eq(1),
        $days_3 = this.$.days.eq(2),
        $hour_1 = this.$.hours.eq(0),
        $hour_2 = this.$.hours.eq(1),
        $min_1  = this.$.minutes.eq(0),
        $min_2  = this.$.minutes.eq(1),
        $sec_1  = this.$.seconds.eq(0),
        $sec_2  = this.$.seconds.eq(1);


        this.countdown_interval = setInterval(function() {

        if(that.total_seconds > 0) {

            --that.values.seconds;

            if(that.values.minutes >= 0 && that.values.seconds < 0) {

                that.values.seconds = 59;
                --that.values.minutes;
            }

            if(that.values.hours >= 0 && that.values.minutes < 0) {

                that.values.minutes = 59;
                --that.values.hours;
            }

            // Update DOM values
            // Hours
            const second = 1000,
            minute = second * 60,
            hour = minute * 60,
            day = hour * 24;

            let countDown = new Date('Nov 17, 2019 17:00:00').getTime()
            let now = new Date().getTime();
            var distance = countDown - now;



            var days_mine = Math.floor(distance / (day));
            var hours_mine = Math.floor((distance % (day)) / (hour));
            var minutes_mine = Math.floor((distance % (hour)) / (minute));
            var seconds_mine = Math.floor((distance % (minute)) / second);

            that.checkDay(days_mine, $days_1, $days_2, $days_3);

            that.checkHour(hours_mine, $hour_1, $hour_2);

            // Minutes
            that.checkHour(minutes_mine, $min_1, $min_2);

            // Seconds
            that.checkHour(seconds_mine, $sec_1, $sec_2);


            --that.total_seconds;
        }
        else {
            clearInterval(that.countdown_interval);
        }
    }, 1000);
  },

  animateFigure: function($el, value) {

     var that         = this,
		     $top         = $el.find('.top'),
         $bottom      = $el.find('.bottom'),
         $back_top    = $el.find('.top-back'),
         $back_bottom = $el.find('.bottom-back');

    // Before we begin, change the back value
    $back_top.find('span').html(value);

    // Also change the back bottom value
    $back_bottom.find('span').html(value);

    // Then animate
    TweenMax.to($top, 0.8, {
        rotationX           : '-180deg',
        transformPerspective: 300,
	      ease                : Quart.easeOut,
        onComplete          : function() {

            $top.html(value);

            $bottom.html(value);

            TweenMax.set($top, { rotationX: 0 });
        }
    });

    TweenMax.to($back_top, 0.8, {
        rotationX           : 0,
        transformPerspective: 300,
	      ease                : Quart.easeOut,
        clearProps          : 'all'
    });
  },

  checkHour: function(value, $el_1, $el_2) {

    var val_1       = value.toString().charAt(0),
        val_2       = value.toString().charAt(1),
        fig_1_value = $el_1.find('.top').html(),
        fig_2_value = $el_2.find('.top').html();

    if(value >= 10) {

        // Animate only if the figure has changed
        if(fig_1_value !== val_1) this.animateFigure($el_1, val_1);
        if(fig_2_value !== val_2) this.animateFigure($el_2, val_2);
    }
    else {

        // If we are under 10, replace first figure with 0
        if(fig_1_value !== '0') this.animateFigure($el_1, 0);
        if(fig_2_value !== val_1) this.animateFigure($el_2, val_1);
    }
  },

  checkDay: function(value, $el_1, $el_2, $el_3 ) {

    var val_1       = value.toString().charAt(0),
        val_2       = value.toString().charAt(1),
        val_3       = value.toString().charAt(2),
        fig_1_value = $el_1.find('.top').html(),
        fig_2_value = $el_2.find('.top').html();
        fig_3_value = $el_3.find('.top').html();

    if(value >= 10) {

        // Animate only if the figure has changed
        if(fig_1_value !== val_1) this.animateFigure($el_1, val_1);
        if(fig_2_value !== val_2) this.animateFigure($el_2, val_2);
        if(fig_3_value !== val_3) this.animateFigure($el_3, val_3);
    }
    else {

        // If we are under 10, replace first figure with 0
        if(fig_1_value !== '0') this.animateFigure($el_1, 0);
        if(fig_2_value !== val_1) this.animateFigure($el_2, val_1);
    }
  }


};

// Let's go !
Countdown.init();
