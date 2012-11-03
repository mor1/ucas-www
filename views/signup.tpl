%# 
<form>
  <fieldset>
    <legend>
      Enter your details and select a slot.
    </legend>

    <ol>
      <li>
        <label for="ucasid">UCAS Id</label>
        <input type="text" name="ucasid" />
      </li>
      <li>
        <label for="name">Name</label>
        <input type="text" name="name" />
      </li>
      <li>
        <fieldset>
          <legend>Available slots</legend>
%for slot in slots:
          <label>
            <input type="radio" name="slot" value="{{ slot['value'] }}" />  
            {{ slot['display'] }}
          </label>
%end
        </fieldset>
      </li>
    </ol>
    <input type="submit" value="Submit" />
  </fieldset>
</form>

%rebase layout title="Sign-up"
