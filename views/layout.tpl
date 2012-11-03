<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="description" content="UCAS small group discussion sign-up" />
    <meta name="author" content="Richard Mortier" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    
    <!-- Le HTML5 shim, for IE6-8 support of HTML elements -->
    <!--[if lt IE 9]>
        <script 
        src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->

    <link rel="stylesheet" media="screen" type="text/css" 
          href="/css/ucas.css" 
          />
    
    <!-- google analytics async -->
    <script type="text/javascript">
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-35396848-2']);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); 
  ga.type = 'text/javascript'; 
  ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 
       'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; 
  s.parentNode.insertBefore(ga, s);
})();
    </script>
    
    <title>
      {{title or 'No title'}}
    </title>
  </head>

  <body>
    <div id="header">
      %include header title='{{ title }}'
    </div>
    
    %include
    
    <div id="footer">
      %include footer error=error
    </div>
  </body>
</html>
