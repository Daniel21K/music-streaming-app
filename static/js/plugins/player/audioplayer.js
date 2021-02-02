Object.defineProperty(HTMLMediaElement.prototype, 'playing', {
    get: function () {
        return !!(this.currentTime > 0 && !this.paused && !this.ended && this.readyState > 2);
    }
})

$(document).ready(function () {
    const $musicPlayer = document.getElementById('musicPlayer');
    if ($musicPlayer != null) {
        (function () {

            /*---- Play / Pause Toggle ----*/

            function play() {
                // checking.. the song is playing or not
                if ($('#play').hasClass('pause')) {
                    $musicPlayer.pause()
                } else {
                    $musicPlayer.play()
                }
                $('#play').toggleClass('pause');
            }
            $('#play').click(play);

            /*---- Convert Audio Duration (Sec) into MM : SS ----*/

            function getDurMin($sec) {
                // if($sec.isNaN()){}
                var min = parseInt($sec / 60);
                var sec = parseInt($sec % 60);
                if (min < 10) {
                    min = '0' + min;
                }
                if (sec < 10) {
                    sec = '0' + sec;
                }
                return { min: min, sec: sec };
            }

            /*---- Update duration into DOM in MM : SS format ----*/

            var timeDrag = false;
            $('.jp-play-bar').mousedown(function(e) {
                timeDrag = true;
                updatebar(e.pageX);

            });
            $(document).mouseup(function(e) {
                if (timeDrag) {
                    timeDrag = false;
                    updatebar(e.pageX);
                }
            });
            $(document).mousemove(function(e) {
                if (timeDrag) {
                    updatebar(e.pageX);
                }
            });

            var updatebar = function(x) {
                var progress = $('.jp-progress');
                var position = x - progress.offset().left;
                var percentage = 100 * position / progress.width();
                if (percentage > 100) {
                    percentage = 100;
                }
                if (percentage < 0) {
                    percentage = 0;
                }
                $("#jquery_jplayer_1").jPlayer("duration-range-thumb", percentage);
                $('.jp-play-bar').css('width', percentage + '%');
            };

            /*---- Repeat Control Starts ----*/

            $('#repeat').click(function () {
                // if (!$musicPlayer.playing) { play() }
                if ($(this).hasClass('looped')) {
                    $musicPlayer.loop = false
                    $(this).removeClass('looped')
                } else {
                    $musicPlayer.loop = true
                    $(this).addClass('looped')
                }
            })


            /*---- Volume Control Starts ----*/

            $('.knob-wrapper').mousedown(function() {
                $(window).mousemove(function(e) {
                    var angle1 = getRotationDegrees($('.knob')),
					volume = angle1 / 270

                    if (volume > 1) {
                        $("#musicPlayer").jPlayer("volume", 1);
                    } else if (volume <= 0) {
                        $("#musicPlayer").jPlayer("mute");
                    } else {
                        $("#musicPlayer").jPlayer("volume", volume);
                        $("#musicPlayer").jPlayer("unmute");
                    }
                });

                return false;
            }).mouseup(function() {
                $(window).unbind("mousemove");
            });


			function getRotationDegrees(obj) {
				var matrix = obj.css("-webkit-transform") ||
				obj.css("-moz-transform")    ||
				obj.css("-ms-transform")     ||
				obj.css("-o-transform")      ||
				obj.css("transform");
				if(matrix !== 'none') {
					var values = matrix.split('(')[1].split(')')[0].split(',');
					var a = values[0];
					var b = values[1];
					var angle = Math.round(Math.atan2(b, a) * (180/Math.PI));
				} else { var angle = 0; }
				return (angle < 0) ? angle + 360 : angle;
			}


            /*---- Duration Control Starts ----*/
            const $dur_thumb = $('#duration-range-thumb'),
                $dur_bar = $('#duration-range-bar'),
                $dur_main = $('#duration-range-main'),
                $dur_parent = $('#duration-range');

            // Set duration accordingly when clicked anywhere on the range bar
            $dur_main.click(function (e) {
                e.stopPropagation()
                var posX = e.pageX - $(this).offset().left;
                $musicPlayer.currentTime = (posX / $dur_parent.width()) * $musicPlayer.duration;
            })
            // Updates range bar and time (MM : SS) in DOM when playing
            $musicPlayer.ontimeupdate = function () {
                $("#startTime").text(getDurMin(this.currentTime).min + " : " + getDurMin(this.currentTime).sec)
                var curTime = parseInt(this.currentTime)
                var totalTime = parseInt(this.duration);
                var calcPos = ($dur_parent.width() * (curTime / totalTime))
                $dur_bar.width(calcPos)
                if (calcPos <= ($dur_thumb.width() / 2)) {
                    $dur_thumb.css({
                        'left': '0'
                    })
                }
                //    else if (calcPos >= ($dur_parent.width() - $dur_thumb.width())) {
                //         $dur_thumb.css({
                //             'left': ($dur_parent.width() - $dur_thumb.width())
                //         })
                //     }
                else {
                    $dur_thumb.css({
                        'left': calcPos - ($dur_thumb.width() / 2)
                    })
                }
                if ($musicPlayer.playing) {
                    $('#play').addClass('pause')
                } else {
                    $('#play').removeClass('pause')
                }
            }
            // Drag thumb
            var calcDur;
            $dur_thumb.draggable({
                axis: 'x',
                start: function () {
                    $musicPlayer.pause()
                },
                drag: function () {
                    $dur_bar.width(($(this).position().left + ($(this).width() / 2)));
                    calcDur = ($dur_bar.width() / $dur_parent.width()) * $musicPlayer.duration
                    $("#startTime").text(getDurMin(calcDur).min + " : " + getDurMin(calcDur).sec);
                },
                stop: function () {
                    $musicPlayer.currentTime = calcDur
                    $musicPlayer.play();
                },
                containment: [
                    ($dur_parent.offset().left), // x0
                    0,//y0
                    (($dur_parent.offset().left //<-->
                        + $dur_parent.width())  //<--x1-->
                        + $dur_thumb.width() / 2),//<-->
                    0//y1
                ]
            })


            /*---- Duration Control Ends ----*/

            // others

        })();
    }

});