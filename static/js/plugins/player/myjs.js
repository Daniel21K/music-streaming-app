

/*---- Play / Pause Toggle ----*/

            function play() {
                if ($('#play').hasClass('pause')) {
                    $musicPlayer.pause()
                } else {
                    $musicPlayer.play()
                }
                $('#play').toggleClass('pause');
            }
            $('#play').click(play);