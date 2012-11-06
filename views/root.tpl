<p>
  This is the sign-up site for applicants visiting The University of
  Nottingham School of Computer Science UCAS days who wish to take part in a
  small group discussion with a member of staff. We will record your UCAS Id,
  your name, and a contact email address (optional) against the slot for which
  you sign up. Slots are allocated on a first-come first-served basis.
</p>

<p>
  <a class="btn btn-primary" href="{{root}}signup">Sign-up for a slot</a>
</p>

%if booking:
<div id="booking">
  <strong>
    {{ booking['name'] }}
    <small>&lt;{{ booking['email'] }}&gt;, 
    UCAS Id {{ booking['ucasid'] }}
    </small>
  is booked in at {{ booking['slot'] }}
  in {{ booking['room'] }}
  with {{ booking['staffname'] }}
  </strong>
</div>
%else:
<form class="form-horizontal" method="post">
  <fieldset>
    <legend class="small">
      Enter your UCAS Id and name to retrieve your booking
    </legend>
    <div class="control-group">
      <label class="control-label" for="ucasid">UCAS Id</label>
      <div class="controls">
        <input type="text" name="ucasid" autofocus required />
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="name">Name</label>
      <div class="controls">
        <input type="text" name="name" required />
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
%end
%rebase layout root=root, breadcrumbs=breadcrumbs, error=error
