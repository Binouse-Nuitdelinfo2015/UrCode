
<script language="javascript" type="text/javascript">
function playSound(soundfile) {
myAudio = document.getElementById("xwing").innerHTML=
"<embed src=\""+soundfile+"\" hidden=\"true\" autostart=\"true\" loop=\"false\" />";
myAudio.addEventListener('cantplayafter', function() {
    if(this.currentTime > 1){this.stop;}
  });

}
</script>

