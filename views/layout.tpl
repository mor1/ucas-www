<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
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
