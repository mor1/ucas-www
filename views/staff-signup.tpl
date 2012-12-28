<p>
  <a class="btn" href="/staff/logout">logout</a>
  Welcome! You are now logged in.
</p>

<form class="form-horizontal" method="post">
  <fieldset>
    <h4>
      Enter your details and indicate which dates you could support:
    </h4>

    <div class="control-group 
      %if data.error and data.error == "userid-validation":
      error
      %end
      ">
      <label class="control-label" for="userid">CS User Id</label>
      <div class="controls">
        <input type="text" name="userid" placeholder="e.g., rmm" 
               %if staff and 'staffid' in staff:
               value="{{ staff['staffid'] }}"
               %end
               required autofocus 
               />
        <small>required</small>
        %if data.error and data.error == "userid-validation":
        <span class="help-inline">
          <i class="icon-warning-sign"></i>
          invalid CS User Id &ndash; please check and retry
        </span>
        %end
        <input type="submit" class="btn" 
               name="retrieve" value="retrieve existing record" />
      </div>
    </div>

    <div class="control-group">
      <label class="control-label" for="name">Name</label>
      <div class="controls">
        <input type="text" name="name" placeholder="e.g., Richard Mortier"
               %if staff and 'staffname' in staff:
               value="{{ staff['staffname'] }}"
               %end
               />
        <small>required</small>
        %if data.error and data.error == "update-missing-name":
        <span class="help-inline">
          <i class="icon-warning-sign"></i>
          missing user name &ndash; please check and retry
        </span>
        %end
      </div>
    </div>    
  
    <div class="control-group">
      <label class="control-label" for="research">Research</label>
      <div class="controls">
        <input type="text" name="research" class="span6"
               placeholder="e.g., systems and networking"
               %if staff and 'research' in staff:
               value="{{ staff['research'] }}"
               %end
               />
        <small>required</small>
        %if data.error and data.error == "update-missing-research":
        <span class="help-inline">
          <i class="icon-warning-sign"></i>
          missing research &ndash; please check and retry
        </span>
        %end
      </div>
    </div>    
  
    <div class="control-group 
      %if data.error and data.error == "module-validation":
      error
      %end
      ">
      <label class="control-label" for="modules">Modules</label>
      <div class="controls">
        <input type="text" name="modules" placeholder="e.g., G54CCS, G54ACC"
               %if staff and 'modules' in staff:
               value="{{ ", ".join([ m.upper() for m in staff['modules'] ]) }}"
               %end
               />
        <small>required, comma separated</small>
        %if data.error and data.error == "module-validation":
        <span class="help-inline">
          <i class="icon-warning-sign"></i>
          invalid module list &ndash; please check and retry
        </span>
        %end
      </div>
    </div>    
  
    <hr style="margin-bottom: 0" />
    <h4>Dates:</h4>
    
    %for date in staff['dates']:
    <label class="checkbox inline" style="margin-left: 2em">
      <input type="checkbox" name="dateid-{{ date['dateid'] }}" 
             %if 'checked' in date and date['checked']:
             checked="checked"
             %end
             />
      {{ date['date'] }}
    </label>
    %end

  <hr style="margin-bottom: 0" />
  <div class="control-group">
    <div class="form-actions pull-left" style="border-top: none">
      <input type="submit" class="btn span4 btn-primary" value="Submit" />
        %if data.error and data.error == "update-success":
        <span class="help-inline">
          <i class="icon-ok"></i>
          success &ndash; entry updated
        </span>
        %end
    </div>
  </div>
</form>

%rebase layout data=data
