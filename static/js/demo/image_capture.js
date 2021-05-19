    /* JS comes here */
        var count=0;

        var width = 320; // We will scale the photo width to this
        var height = 24; // This will be computed based on the input stream

        var streaming = false;

        var video = null;
        var canvas = null;
        var photo = null;
        var startbutton = null;

        function startup() {
            video = document.getElementById('video');
            canvas = document.getElementById('canvas');
            photo = document.getElementById('photo');
            canvas1 = document.getElementById('canvas1');
            photo1 = document.getElementById('photo1');
            canvas2 = document.getElementById('canvas2');
            photo2 = document.getElementById('photo2');
            canvas3 = document.getElementById('canvas3');
            photo3 = document.getElementById('photo3');
            canvas4 = document.getElementById('canvas4');
            photo4 = document.getElementById('photo4');
            canvas5 = document.getElementById('canvas5');
            photo5 = document.getElementById('photo5');


            




            startbutton = document.getElementById('startbutton');

            navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false
                })
                .then(function(stream) {
                    video.srcObject = stream;
                    video.play();
                })
                .catch(function(err) {
                    console.log("An error occurred: " + err);
                });

            video.addEventListener('canplay', function(ev) {
                if (!streaming) {
                    height = video.videoHeight / (video.videoWidth / width);

                    if (isNaN(height)) {
                        height = width / (4 / 3);
                    }

                    video.setAttribute('width', width);
                    video.setAttribute('height', height);
                    canvas.setAttribute('width', width);
                    canvas.setAttribute('height', height);
                    streaming = true;
                }
            }, false);

            startbutton.addEventListener('click', function(ev) {
                count=count+1;
                if(count==1)
                {
                    takepicture();
                }
                else if(count==2)
                {
                    takepicture1();
                }
                else if(count==3)
                {
                    takepicture2();
                }
                else if(count==4)
                {
                    takepicture3();
                }
                else if(count==5)
                {
                    takepicture4();
                }
                else if(count==6)
                {
                    takepicture5();
                }





                ev.preventDefault();
            }, false);

        }


        function clearphoto() {
            var context = canvas.getContext('2d');
            context.fillStyle = "#AAA";
            context.fillRect(0, 0, canvas.width, canvas.height);

            var data = canvas.toDataURL('image/png');
            photo.setAttribute('src', data);
        }

        function takepicture() {
            var context = canvas.getContext('2d');
            if (width && height) {
                canvas.width = width;
                canvas.height = height;
                context.drawImage(video, 0, 0, width, height);

                var data = canvas.toDataURL('image/png');
                photo.setAttribute('src', data);
            } else {
                clearphoto();
            }
        }
        function takepicture1() {
            var context = canvas1.getContext('2d');
            if (width && height) {
                canvas1.width = width;
                canvas1.height = height;
                context.drawImage(video, 0, 0, width, height);

                var data = canvas1.toDataURL('image/png');
                photo1.setAttribute('src', data);
            } else {
                clearphoto();
            }
        }
        function takepicture2() {
            var context = canvas2.getContext('2d');
            if (width && height) {
                canvas2.width = width;
                canvas2.height = height;
                context.drawImage(video, 0, 0, width, height);

                var data = canvas2.toDataURL('image/png');
                photo2.setAttribute('src', data);
            } else {
                clearphoto();
            }
        }
        function takepicture3() {
            var context = canvas3.getContext('2d');
            if (width && height) {
                canvas3.width = width;
                canvas3.height = height;
                context.drawImage(video, 0, 0, width, height);

                var data = canvas3.toDataURL('image/png');
                photo3.setAttribute('src', data);
            } else {
                clearphoto();
            }
        }
        function takepicture4() {
            var context = canvas4.getContext('2d');
            if (width && height) {
                canvas4.width = width;
                canvas4.height = height;
                context.drawImage(video, 0, 0, width, height);

                var data = canvas4.toDataURL('image/png');
                photo4.setAttribute('src', data);
            } else {
                clearphoto();
            }
        }


        function takepicture5() {
            var context = canvas5.getContext('2d');
            if (width && height) {
                canvas5.width = width;
                canvas5.height = height;
                context.drawImage(video, 0, 0, width, height);

                var data = canvas5.toDataURL('image/png');
                photo5.setAttribute('src', data);
            } else {
                clearphoto();
            }
        }

        function download(){
        
            var download = document.getElementById("download");
            
            var image = document.getElementById("canvas").toDataURL("image/png")
                        .replace("image/png", "image/octet-stream");
            download.setAttribute("href", image);
    
        }
    

//         function upload() {
//             console.log("Uploading...")
//             alert("jai")
//             var image = document.getElementById('photo').src;
//             var form = document.getElementById('myform');
//             var formData = new FormData(form);
//             formData.append("file", picture);
//             var xmlhttp = new XMLHttpRequest();
//             xmlhttp.open("POST", "/upload");
        
//             // check when state changes, 
//             xmlhttp.onreadystatechange = function() {
        
//             if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
//                 alert(xmlhttp.responseText);
//                 }
//             }
        

        
//             xmlhttp.send(formData);
//         var fs = require('fs'); 
//         var imagedata // get imagedata from POST request 
//         fs.writeFile("/images/file.png", imagedata, 'binary', function(err) { 
//         console.log("The file was saved!"); 
 
// });  
//             console.log(formData.get('upload'));
//             console.log(formData.get('username'));
//             console.log("jai")
//         }
        

        window.addEventListener('load', startup, false);
    ;