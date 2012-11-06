<h1>
  UCAS Small Group Discussion Sign-up
</h1>
<h2>
  School of Computer Science, The University of Nottingham
</h2>

<p>
  This is the sign-up site for applicants visiting UCAS days who wish to take
  part in a small group discussion with a member of staff. We will record your
  UCAS Id, your name, and a contact email address (optional) against the slot
  for which you sign up. Slots are allocated on a first-come first-served
  basis.
</p>

<p>
  <a href="/signup">Sign-up for a slot</a>
</p>

<form method="post">
  <fieldset>
    <legend>Enter your UCAS Id and name to retrieve your booking</legend>
    <ol>
      <li>
        <label for="ucasid">UCAS Id</label>
        <input type="text" name="ucasid" autofocus required />
      </li>
      <li>
        <label for="name">Name</label>
        <input type="text" name="name" required />
      </li>
    </ol>
    <input type="submit" value="retrieve booking" />
  </fieldset>
</form>

%if booking:
<div id="booking">
  <ol>
    <li>
      <label for="ucasid">UCAS Id</label>
      <span id="ucasid">{{ booking['ucasid'] }}</span>
    </li>
    <li>
      <label for="name">Name</label>
      <span id="name">{{ booking['name'] }}</span>
    </li>
    <li>
      <label for="email">Email</label>
      <span id="email">{{ booking['email'] }}</span>
    </li>
    <li>
      <label for="slot">Slot</label>
      <span id="slot">{{ booking['slot'] }}</span>
    </li>
    <li>
      <label for="room">Room</label>
      <span id="room">{{ booking['room'] }}</span>
    </li>
    <li>
      <label for="staffname">Staffname</label>
      <span id="staffname">{{ booking['staffname'] }}</span>
    </li>
    <li>
      <label for="research">Research</label>
      <span id="research">{{ booking['research'] }}</span>
    </li>
    <li>
      <label for="modules">Modules</label>
      <span id="modules">{{ booking['modules'] }}</span>
    </li>
  </ol>
</div>
%end

%rebase layout title="UCAS Discussion Group Signup", error=error
