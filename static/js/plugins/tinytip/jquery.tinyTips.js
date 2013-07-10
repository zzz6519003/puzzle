/***********************************************************/
/*                    TinyTips Plugin                      */
/*                      Version: 1.3                       */
/*                      Mike Merritt                       */
/*         https://github.com/mikemerritt/TinyTips         */
/***********************************************************/

(function($) {
	$.fn.tinyTips = function(options) {
		
		var defaults = {
			content: 'tt',
			position: 'top',
			spacing: 8,
			transition: 'fade',
			arrow: true,
			arrowColor: 'rgba(0, 0, 0, 0.8)'
		};

		options = $.extend(defaults, options);


		var markup = '<div id="tinytip"><div class="arrow"></div></div>';
		var tip;

		// Calculates where to put the tip to keep it from extending off screen. 
		calcPos = function(side, target, tip) {

			var finalPos = {
				x: 0,
				y: 0,
				fPos: '',
			};

			var posCheck = {
				top: true,
				bottom: true,
				left: true,
				right: true
			}

			var pos = {
				top: {
					x: target.x-(tip.outerWidth()/2)+(target.w/2),
					y: target.y-options.spacing
				},
				right: {
					x: target.x+target.w+options.spacing,
					y: target.y+(tip.outerHeight()/2)+(target.h/2)
				},
				bottom: {
					x: target.x-(tip.outerWidth()/2)+(target.w/2),
					y: target.y+tip.outerHeight()+target.h+options.spacing
				},
				left: {
					x: target.x-tip.outerWidth()-options.spacing,
					y: target.y+(tip.outerHeight()/2)+(target.h/2)
				}
			};

			if (pos.top.y-tip.outerHeight() < $(window).scrollTop()) {
				posCheck.top = false;
			}

			if (pos.bottom.y+tip.outerHeight() > $(window).height()+$(window).scrollTop()) {
				posCheck.bottom = false;
			}
			
			if (pos.left.x < 0) {
				posCheck.left = false;
			}


			if (pos.right.x+tip.outerWidth() > $(window).width()) {
				posCheck.right = false;
			}

			if (side === 'top' || side ==='bottom' || posCheck.left === false || posCheck.right === false) {
				if (pos.top.x < 0) {
					posCheck.top = false;
					posCheck.bottom = false;
				} else if (pos.top.x+tip.outerWidth() > $(window).width()) {
					posCheck.top = false;
					posCheck.bottom = false;
				}
			}

			if (posCheck[side] === true) {
				finalPos.x = pos[side].x;
				finalPos.y = pos[side].y;
				finalPos.fPos = side;
				return finalPos;
			} else {
				for(var s in posCheck) {
					if (posCheck[s] === true) {
						finalPos.x = pos[s].x;
						finalPos.y = pos[s].y;
						finalPos.fPos = s;
						break;
					}
				}
			}
			return finalPos;
		}

		$(this).on("mouseover", function() {
			$('body').prepend(markup);
			tip = $('#tinytip');
			tip.hide()

			tip.css({top: 0, left: 0});

            if($.isFunction(options.content)){
                console.log(options.content($(this)));
			    tip.append(options.content($(this)));
            }else{
			    tip.append($(this).attr('tt'));
            }

			var pos = $(this).position();

			var target = {
				y: pos.top,
				x: pos.left,
				w: $(this).outerWidth(),
				h: $(this).outerHeight()
			};

			var ttPos = calcPos(options.position, target, tip);

			var tt = {
				x: ttPos.x,
				y: ttPos.y,
				w: tip.outerWidth(),
				h: tip.outerHeight(),
				fPos: ttPos.fPos
			}

			// Place arrow
			if (options.arrow === true) {
				finalSpacing = (options.spacing+6)/2;

				if (tt.fPos === 'top') {					
					$('#tinytip .arrow').css({
						borderColor: options.arrowColor + ' transparent', 
						borderWidth: '6px 6px 0 6px', 
						bottom: '-6px',
						left: '50%'
					});
				} else if (tt.fPos === 'bottom') {
					$('#tinytip .arrow').css({
						borderColor: 'transparent transparent ' + options.arrowColor + ' transparent', 
						borderWidth: '0 6px 6px 6px', 
						top: '-6px',
						left: '50%'
					});
				} else if (tt.fPos === 'left') {
					$('#tinytip .arrow').css({
						borderColor: 'transparent transparent transparent' + options.arrowColor, 
						borderWidth: '6px 0 6px 6px', 
						top: ((tt.h/2)-6)+'px',
						right: '-6px'
					});
				} else if (tt.fPos === 'right') {
					$('#tinytip .arrow').css({
						borderColor: 'transparent rgba(0, 0, 0, 0.8) transparent transparent', 
						borderWidth: '6px 6px 6px 0', 
						top: ((tt.h/2)-6)+'px',
						left: '-6px'
					});
				}

			} else if (options.arrow === false) {
				finalSpacing = options.spacing/2;
				$('#tinytip .arrow').remove();
			}

            animationDuration = 300;

			// Animate tip
			if (tt.fPos === 'top') {
				tip.show(animationDuration).css({opacity: 0, top: tt.y-tt.h+finalSpacing+'px', left: tt.x+'px'});
			} else if (tt.fPos === 'bottom') {
				tip.show(animationDuration).css({opacity: 0, top: tt.y-tt.h-finalSpacing+'px', left: tt.x+'px'});
			} else if (tt.fPos === 'left') {
				tip.show(animationDuration).css({opacity: 0, top: tt.y-tt.h+'px', left: tt.x+finalSpacing+'px'});
			} else if (tt.fPos === 'right') {
				tip.show(animationDuration).css({opacity: 0, top: tt.y-tt.h+'px', left: tt.x-finalSpacing+'px'});
			}
			
			tip.animate({top: tt.y-tt.h, left: tt.x, opacity: 1});

		});

		$(this).on("mouseout", function() {
			tip.stop().hide();
			tip.text("");
			tip.remove();

		});
	};
})(jQuery);
