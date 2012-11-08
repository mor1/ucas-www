<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="description" content="UCAS Group Discussion Sign-up" />
    <meta name="author" content="Richard Mortier" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    
    <!-- Le HTML5 shim, for IE6-8 support of HTML elements -->
    <!--[if lt IE 9]>
        <script 
        src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->

    <link rel="stylesheet" media="screen" type="text/css" 
          href="{{ data.root }}css/ucas.css" 
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
      UCAS Discussion Group Sign-up
    </title>
  </head>

  <body>
    <div class="navbar navbar-inverse navbar-static-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>

          <a class="brand" href="{{ data.root }}">
            UCAS Discussion Group Sign-up
          </a>

        </div>
      </div>
    </div>

    <div class="container-fluid">
          <ul class="breadcrumb">
%for bc in data.breadcrumbs[:-1]:
            <li>
              <a href="{{ bc[1] }}">{{ bc[0] }}</a> 
              <span class="divider">/</span>
            </li>
%end
            <li class="active">{{ data.breadcrumbs[-1][0] }}</li>
          </ul>

      %include

      <footer>
%if data.error:
        <div id="error">
          <p>
            ERROR! {{ data.error }}
          </p>
        </div>
%end
        <div class="well well-small muted">
          <div id="contact">
            Please contact <a href="mailto:admissions@cs.nott.ac.uk">
            admissions@cs.nott.ac.uk</a> if you have any questions about this
            process. 

            <br /> 

            Please contact <a href="mailto:richard.mortier@nottingham.ac.uk">
            richard.mortier@nottingham.ac.uk</a> if you experience any
            problems with this website.
          </div>
        </div>
        <div class="pull-right">
          <small>Copyright &copy; 2012, Richard Mortier.</small>
        </div>
      </footer>
    </div>
  </body>
</html>
