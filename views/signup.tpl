<p>
  We will record your UCAS Personal Number and your name against the slot for
  which you sign up. Slots are allocated on a first-come first-served basis.
</p>

%if len(slots) == 0:
<p>
  Sorry! We have no upcoming UCAS visit dates with small group discussions
  scheduled at this time. We will be updating this soon, so please do check
  back or <a href="mailto:admissions@cs.nott.ac.uk">email us</a> if you wish
  to register interest now.
</p>
%else:
<hr />
<form class="form-horizontal" method="post">
  <fieldset>
    <h4>
      Enter your details and select a slot:
    </h4>

    <div class="control-group 
%if data.error and data.error == "ucasid-validation":
      error
%end
      ">
      <label class="control-label" for="ucasid">UCAS Personal Number</label>
      <div class="controls">
        <input type="text" name="ucasid" placeholder="e.g., 123-456-7890"
               required autofocus />
        <small>required</small>
%if data.error and data.error == "ucasid-validation":
        <span class="help-inline">
          <i class="icon-warning-sign"></i>
          invalid UCAS Personal Number &ndash; please check and retry
        </span>
%end
      </div>
    </div>    
    <div class="control-group
%if data.error and data.error in ("booking-mismatch", "name-validation"):
      error
%end
      ">
      <label class="control-label" for="name">Name</label>
      <div class="controls">
        <input type="text" name="name" required />
        <small>required</small>
%if data.error and data.error == "booking-mismatch":
        <span class="help-inline">
          <i class="icon-warning-sign"></i>
          details don't match &ndash; please check and retry
        </span>
%elif data.error and data.error == "name-validation":
        <span class="help-inline">
          <i class="icon-warning-sign"></i>
          <i>Name</i> cannot be blank &ndash; please complete and retry
        </span>
%end
      </div>
    </div>
  </fieldset>

  <fieldset>
    <strong>Available slots:</strong>
    <label class="radio">
      <input type="radio" name="slotid" value="{{ slots[0]['slotid'] }}"
             checked />
      <small>at</small> {{ slots[0]['date'] }}
      <small>in</small> {{ slots[0]['room'] }}
      <small>with</small> {{ slots[0]['staffname'] }}
      <small>who teaches</small> 
      %for module in slots[0]['modules'][:-1]:
      <a href="{{ base_url }}?crs_id={{ module['crsid'] }}&year_id=000112">{{ module['code'] }}</a>, 
      %end
      <a href="{{ base_url }}?crs_id={{ slots[0]['modules'][-1]['crsid'] }}&year_id=000112">{{ slots[0]['modules'][-1]['code'] }}</a>
      <br />&nbsp;&nbsp;&nbsp;
      <small>and can talk about</small> {{ slots[0]['research'] }}.
      <br />
      <small>({{ slots[0]['spaces'] }} places remaining)</small>
    </label>
%for slot in slots[1:]:
    <label class="radio">
      <input type="radio" name="slotid" value="{{ slot['slotid'] }}" />
      <small>at</small> {{ slot['date'] }}
      <small>in</small> {{ slot['room'] }}
      <small>with</small> {{ slot['staffname'] }}
      <small>who teaches</small>
      %for module in slot['modules'][:-1]:
      <a href="{{ base_url }}?crs_id={{ module['crsid'] }}&year_id=000112">{{ module['code'] }}</a>, 
      %end
      %if len(slot['modules']) > 0:
      <a href="{{ base_url }}?crs_id={{ slot['modules'][-1]['crsid'] }}&year_id=000112">{{ slot['modules'][-1]['code'] }}</a>
      %end
      <br />&nbsp;&nbsp;&nbsp;
      <small>and can talk about</small> {{ slot['research'] }}.
      <br />
      <small>({{ slot['spaces'] }} places remaining)</small>
    </label>
%end
  </fieldset>

  <hr style="margin-bottom: 0" />
  <div class="control-group">
    <div class="form-actions pull-left" style="border-top: none">
      <input type="submit" class="btn span4 btn-primary" value="Submit" />
    </div>
  </div>
</form>
%end

%rebase layout data=data, slots=slots
