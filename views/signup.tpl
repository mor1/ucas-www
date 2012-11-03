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
%for slot in slots:
          <label>
            <input type="radio" name="slotid" value="{{ slot['slotid'] }}" />
            {{ slot['slot'] }}
            {{ slot['spaces'] }}
          </label>
%end
        </fieldset>
      </li>
    </ol>
    <input type="submit" value="Submit" />
  </fieldset>
</form>

%rebase layout title="Sign-up", error=error
