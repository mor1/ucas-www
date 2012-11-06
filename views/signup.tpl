%if len(slots) == 0:
<p>
  Sorry! No remaining slots.
</p>
%else:
<form method="post">
  <fieldset>
    <legend>
      Enter your details and select a slot.
    </legend>

    <ol>
      <li>
        <label for="ucasid">UCAS Id</label>
        <input type="text" name="ucasid" required autofocus />
      </li>
      <li>
        <label for="name">Name</label>
        <input type="text" name="name" required />
      </li>
      <li>
        <label for="email">Contact Email</label>
        <input type="text" name="email" />
      </li>
      <li>
        <fieldset>
          <legend>Available slots</legend>
          <label>
            <input type="radio" name="slotid" value="{{ slots[0]['slotid'] }}"
                   required checked />
            <ol>
              <li>{{ slots[0]['slot'] }}</li>
              <li>{{ slots[0]['staffname'] }}</li>
              <li>{{ slots[0]['staffid'] }}</li>
              <li>{{ slots[0]['spaces'] }}</li>
              <li>{{ slots[0]['modules'] }}</li>
              <li>{{ slots[0]['research'] }}</li>
            </ol>
          </label>
%for slot in slots[1:]:
          <label>
            <input type="radio" name="slotid" value="{{ slot['slotid'] }}" />
            <ol>
              <li>{{ slot['slot'] }}</li>
              <li>{{ slot['staffname'] }}</li>
              <li>{{ slot['staffid'] }}</li>
              <li>{{ slot['spaces'] }}</li>
              <li>{{ slot['modules'] }}</li>
              <li>{{ slot['research'] }}</li>
            </ol>
          </label>
%end
        </fieldset>
      </li>
    </ol>
    <input type="submit" value="Submit" />
  </fieldset>
</form>
%end

%rebase layout title="Sign-up", error=error
