#include "code.h"
#include <assert.h>
int main(void) {
    assert(!is_admin(0));
    assert(username(0) == NULL);
    assert(!update_setting(0, "0", "1"));
    for (int i = 0; i < MAX_USERS; ++i) {
        int id = create_user_account(false, "student");
        assert(id == i);
        assert(accounts[id]->userid == id);
        assert(!update_setting(id, "-7", "1"));
        assert(!update_setting(id, "10", "1"));
        assert(!update_setting(id, "", "1"));
        assert(!update_setting(id, "0", ""));
        assert(!update_setting(id, "0", "999999999999999999999999"));
        assert(!update_setting(id, NULL, "1"));
        assert(update_setting(id, "9", "42"));
        assert(accounts[id]->setting[9] == 42);
        assert(!is_admin(id));
    }
    assert(create_user_account(false, "extra") == INVALID_USER_ID);
    for (int i = 0; i < MAX_USERS; ++i) free(accounts[i]);
    puts("C bounds, parsing, account capacity, and privilege regressions: PASS");
    return 0;
}
