<div class="well">
  <p>
    This is the sign-up site for applicants visiting The University of
    Nottingham School of Computer Science UCAS days who wish to take part in a
    small group discussion with a member of staff. 
  </p>

  <div>
    <a class="btn btn-primary" href="{{ data.root }}signup">
      sign-up for a slot
    </a>
  </div>
</div>

%if booking:
<div id="booking" class="well">
  <strong>
    {{ booking['name'] }}
    <small>
      UCAS Id {{ booking['ucasid'] }}
    </small>
    is booked in at {{ booking['slot'] }}
    in {{ booking['room'] }}
    with {{ booking['staffname'] }}
  </strong>
</div>
%else:
<div class="well">
  <form class="form-horizontal" method="post">
    <fieldset>
      <p>
        If you have previously signed up, enter your UCAS Id and name to
        retrieve your booking:
      </p>
      <div class="control-group
%if data.error and data.error == "booking-mismatch":
      error
%end
      ">
        <label class="control-label" for="ucasid">UCAS Id</label>
        <div class="controls">
          <input type="text" name="ucasid" placeholder="e.g., 123-456-7890"
                 autofocus required />
          <small>required</small>
%if data.error and data.error == "booking-mismatch":
          <span class="help-inline">
            <i class="icon-warning-sign"></i>
            details don't match &ndash; please check and retry
          </span>
%end
        </div>
      </div>
      <div class="control-group
%if data.error and data.error == "booking-mismatch":
      error
%end
      ">
        <label class="control-label" for="name">Name</label>
        <div class="controls">
          <input type="text" name="name" required />
        <small>required</small>
        </div>
      </div>
    </fieldset>
    <div class="control-group">
      <div class="controls">
        <button type="submit" class="btn">
          retrieve booking
        </button>
      </div>
    </div>
  </form>
</div>
%end

%rebase layout data=data, booking=booking
