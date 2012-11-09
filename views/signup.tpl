<p>
  We will record your UCAS Personal Number and your name against the slot for
  which you sign up. Slots are allocated on a first-come first-served basis.
</p>

%if len(slots) == 0:
<p>
  Sorry! No remaining slots.
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
      <small>at</small> {{ slots[0]['slot'] }}
      <small>with</small> {{ slots[0]['staffname'] }}
      <small>who teaches</small> {{ slots[0]['modules'] }}
      <small>and researches</small> {{ slots[0]['research'] }}
      <small>({{ slots[0]['spaces'] }} places remaining)</small>
    </label>
%for slot in slots[1:]:
    <label class="radio">
      <input type="radio" name="slotid" value="{{ slot['slotid'] }}" />
      <small>at</small> {{ slot['slot'] }}
      <small>with</small> {{ slot['staffname'] }}
      <small>who teaches</small> {{ slot['modules'] }}
      <small>and researches</small> {{ slot['research'] }}
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
