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
            {{ slots[0]['slot'] }}
            {{ slots[0]['name'] }}
            {{ slots[0]['staffid'] }}
            {{ slots[0]['spaces'] }}
            {{ slots[0]['modules'] }}
            {{ slots[0]['research'] }}
          </label>
%for slot in slots[1:]:
          <label>
            <input type="radio" name="slotid" value="{{ slot['slotid'] }}" />
            {{ slot['slot'] }}
            {{ slot['name'] }}
            {{ slot['staffid'] }}
            {{ slot['spaces'] }}
            {{ slot['modules'] }}
            {{ slot['research'] }}
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
