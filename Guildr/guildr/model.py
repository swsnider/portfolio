from datetime import datetime
import pkg_resources
pkg_resources.require("SQLObject>=0.8,<=0.10.0")
from turbogears.database import PackageHub
# import some basic SQLObject classes for declaring the data model
# (see http://www.sqlobject.org/SQLObject.html#declaring-the-class)
from sqlobject import SQLObject, SQLObjectNotFound, RelatedJoin
# import some datatypes for table columns from SQLObject
# (see http://www.sqlobject.org/SQLObject.html#column-types for more)
from sqlobject import StringCol, UnicodeCol, IntCol, DateTimeCol, ForeignKey, MultipleJoin, BoolCol, EnumCol
from turbogears import identity

__connection__ = hub = PackageHub('guildr')

class PluginConfig(SQLObject):
    setting = UnicodeCol(length=255,notNone=True)
    value = UnicodeCol(notNone=True)
    plugin = ForeignKey("Plugin")
    guser = ForeignKey("GuildUser")

class PluginDatum(SQLObject):
    name = UnicodeCol(length=255, notNone=True)
    value = UnicodeCol(notNone=True)
    plugin = ForeignKey("Plugin")
    guser = ForeignKey("GuildUser")

class Plugin(SQLObject):
    name = UnicodeCol(length=255,notNone=True)
    guilds = RelatedJoin('Guild', joinColumn='plugin_id',
                              intermediateTable='guild_plugin',
                              otherColumn='guild_id')
    configs = MultipleJoin("PluginConfig")
    data = MultipleJoin("PluginDatum")
    file = UnicodeCol(notNone=True)

class GuildUser(SQLObject):
    tuser = ForeignKey("User")
    guild = ForeignKey("Guild")
    access = EnumCol(enumValues=["regular","admin"],default="regular",notNone=True)
    configs = MultipleJoin("PluginConfig")
    data = MultipleJoin("PluginDatum")

class Guild(SQLObject):
    members = MultipleJoin("GuildUser")
    disabled = BoolCol(notNone=True,default=False)
    name = UnicodeCol(length=255, notNone=True)
    website = UnicodeCol(length=255, notNone=True,default="")
    plugins = RelatedJoin('Plugin', joinColumn='guild_id',
                              intermediateTable='guild_plugin',
                              otherColumn='plugin_id')

class Visit(SQLObject):
    """
    A visit to your site
    """
    class sqlmeta:
        table = 'visit'

    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()

    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)


class VisitIdentity(SQLObject):
    """
    A Visit that is link to a User object
    """
    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    user_id = IntCol()


class Group(SQLObject):
    """
    An ultra-simple group definition.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_group'

    group_name = UnicodeCol(length=16, alternateID=True,
                            alternateMethodName='by_group_name')
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)

    # collection of all users belonging to this group
    users = RelatedJoin('User', intermediateTable='user_group',
                        joinColumn='group_id', otherColumn='user_id')

    # collection of all permissions for this group
    permissions = RelatedJoin('Permission', joinColumn='group_id',
                              intermediateTable='group_permission',
                              otherColumn='permission_id')


class User(SQLObject):
    """
    Reasonably basic User definition.
    Probably would want additional attributes.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_user'

    user_name = UnicodeCol(length=16, alternateID=True,
                           alternateMethodName='by_user_name')
    email_address = UnicodeCol(length=255, alternateID=True,
                               alternateMethodName='by_email_address')
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)

    # groups this user belongs to
    groups = RelatedJoin('Group', intermediateTable='user_group',
                         joinColumn='user_id', otherColumn='group_id')

    guilds = MultipleJoin("GuildUser")
    banned = BoolCol(notNone=True,default=False)

    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms |= set(g.permissions)
        return perms

    def _set_password(self, cleartext_password):
        """Runs cleartext_password through the hash algorithm before saving."""
        password_hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(password_hash)

    def set_password_raw(self, password):
        """Saves the password as-is to the database."""
        self._SO_set_password(password)


class Permission(SQLObject):
    """
    A relationship that determines what each Group can do
    """
    permission_name = UnicodeCol(length=16, alternateID=True,
                                 alternateMethodName='by_permission_name')
    description = UnicodeCol(length=255)

    groups = RelatedJoin('Group',
                         intermediateTable='group_permission',
                         joinColumn='permission_id',
                         otherColumn='group_id')