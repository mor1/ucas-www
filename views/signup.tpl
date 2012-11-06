%if len(slots) == 0:
<p>
  Sorry! No remaining slots.
</p>
%else:
<form class="form-horizontal" method="post">
  <fieldset>
    <legend class="small">
      Enter your details and select a slot.
    </legend>

    <div class="control-group">
      <label class="control-label" for="ucasid">UCAS Id</label>
      <div class="controls">
        <input type="text" name="ucasid" required autofocus />
      </div>
    </div>    
    <div class="control-group">
      <label class="control-label" for="name">Name</label>
      <div class="controls">
        <input type="text" name="name" required />
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="email">Contact Email</label>
      <div class="controls">
        <input type="text" name="email" />
      </div>
    </div>
  </fieldset>

  <fieldset>
    <legend>Available slots</legend>
    <label class="radio">
      <input type="radio" name="slotid" value="{{ slots[0]['slotid'] }}"
             checked />
      <small>at</small> {{ slots[0]['slot'] }}
      <small>with</small> {{ slots[0]['staffname'] }}
      <small>who teaches</small> {{ slots[0]['modules'] }}
      <small>and researches</small> {{ slots[0]['research'] }}
    </label>
%for slot in slots[1:]:
    <br />
    <label class="radio">
      <input type="radio" name="slotid" value="{{ slot['slotid'] }}" />
      <small>at</small> {{ slot['slot'] }}
      <small>with</small> {{ slot['staffname'] }}
      <small>who teaches</small> {{ slot['modules'] }}
      <small>and researches</small> {{ slot['research'] }}
    </label>
%end
    
  </fieldset>

  <div class="control-group">
    <div class="form-actions">
      <input type="submit" class="btn btn-block btn-primary" value="Submit" />
    </div>
  </div>
</form>
%end

%rebase layout root=root, breadcrumbs=breadcrumbs, error=error
