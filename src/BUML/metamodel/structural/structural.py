from abc import ABC, abstractmethod 
from typing import Any
 
# constant
UNLIMITED_MAX_MULTIPLICITY = 9999

class Element(ABC):
    pass

class NamedElement(Element):
    """The NamedElement is the Superclass of all structural elements with a name.

    Args:
        name (str): the name of the named element
        visibility: Determines the kind of visibility of the named element (public as default).

    Attributes:
        name (str): The name of the named element
        visibility: Determines the kind of visibility of the named element (public as default).

    Raises:
        ValueError: (Invalid visibility) if an invalid visibility is provided.
    """

    def __init__(self, name: str, visibility: str = "public"):
        self.name: str = name
        self.visibility = visibility

    @property
    def name(self) -> str:
        """str: Get the name of the named element."""
        return self.__name

    @name.setter
    def name(self, name: str):
        """str: Set the name of the named element."""
        self.__name = name

    @property
    def visibility(self) -> str:
        """str: Get the visibility of the named element."""
        return self.__visibility

    @visibility.setter
    def visibility(self, visibility: str):
        """str: Set the visibility of the named element. The allowed visibility values 
        are public, private, protected, or package"""
        if visibility not in ['public', 'private', 'protected', 'package']:
            raise ValueError("Invalid visibility")
        self.__visibility = visibility

class Type(NamedElement):
    """Type is the Superclass of classes and data types in the model.

    Args:
        name (str): the name of the Type.

    Attributes:
        name (str): The name of the Type.
    """

    def __init__(self, name: str):
        super().__init__(name)

    def __repr__(self):
        return f"Name({self.name})"

class DataType(NamedElement):
    """Represents a data type.

    This class inherits from NamedElement and is used to model data types.

    Args:
        name (str): The name of the data type.

    Attributes:
        name (str): The name of the data type.
    """

    def __init__(self, name: str):
        super().__init__(name)

class PrimitiveDataType(DataType):
    """Class representing a primitive data type.

    This class is a subclass of DataType and is used to represent primitive data types
    with a specified name.

    Args:
        name (str): the name of the primitive data type.

    Attributes:
        name (str): the name of the primitive data type.

    Raises:
        ValueError: (Invalid primitive data type) if an invalid primitive data type is provided.
    """    

    def __init__(self, name: str):
        super().__init__(name)

    @NamedElement.name.setter
    def name(self, name: str):
        """str: Set the name of the PrimitiveDataType. The allowed values are int, float, str, 
        bool, time, date, datetime, and timedelta"""
        if name not in ['int', 'float', 'str', 'bool', 'time', 'date', 'datetime', 'timedelta']:
            raise ValueError("Invalid primitive data type")
        # calling the setter of the superclass if there are no errors
        super(PrimitiveDataType, PrimitiveDataType).name.fset(self, name)

class TypedElement(NamedElement):
    """TypedElement is a subclass of NamedElement and is used to represent elements
    that have a specific type.

    Args:
        name (str): The name of the typed element.
        type (Type): The data type of the typed element.

    Attributes:
        name (str): The name of the typed element.
        type (Type): The data type of the typed element.
    """

    def __init__(self, name: str, type: Type):
        super().__init__(name)
        self.type: Type = type

    @property
    def type(self) -> Type:
        return self.__type

    @type.setter
    def type(self, type: Type):
        self.__type = type

class Multiplicity:
    """Represents the multiplicity of a Property.

    It consists of a minimum and maximum value, indicating the allowed range.

    Args:
        min (int): The minimum multiplicity.
        max (int): The maximum multiplicity. Use "*" for unlimited.

    Attributes:
        min (int): The minimum multiplicity.
        max (int): The maximum multiplicity. Use "*" for unlimited.
    """

    def __init__(self, min_multiplicity: int, max_multiplicity: int):
        self.min: int = min_multiplicity
        self.max: int = max_multiplicity

    @property
    def min(self) -> int:
        """int: Get the minimum multiplicity."""
        return self.__min

    @min.setter
    def min(self, min_multiplicity: int):
        """int: Set the minimum multiplicity (must be greater than or equal to zero)."""
        if min_multiplicity < 0:
            raise ValueError("Invalid min multiplicity")
        self.__min = min_multiplicity

    @property
    def max(self) -> int:
        """int: Get the maximum multiplicity."""
        return self.__max

    @max.setter
    def max(self, max_multiplicity: int):
        """int: Set the maximum multiplicity. (must be greater than or equal to minimum multiplicity)."""
        if max_multiplicity == "*":
            max_multiplicity = UNLIMITED_MAX_MULTIPLICITY
        if max_multiplicity < 0:
            raise ValueError("Invalid max multiplicity")
        if max_multiplicity < self.min:
            raise ValueError("Invalid max multiplicity")
        self.__max = max_multiplicity

    def __repr__(self):
        return f'Multiplicity({self.min},{self.max})'

# Properties are owned by a class or an association and point to a type with a multiplicity
class Property(TypedElement):
    """A property can represents an attribute of a class or an end of an association.

    Properties are owned by a class or an association.

    Args:
        name (str): The name of the property.
        owner (Type): The type that owns the property.
        property_type (Type): The type of the property.
        multiplicity (Multiplicity): The multiplicity of the property.
        visibility (str): The visibility of the property ('public', 'private', etc.).
        is_composite (bool): Indicates whether the property is a composite.
        is_navigable (bool): Indicates whether the property is navigable in a relationship.
        is_aggregation (bool): Indicates whether the property represents an aggregation.

    Attributes:
        name (str): The name of the property.
        owner (Type): The type that owns the property.
        property_type (Type): The type of the property.
        multiplicity (Multiplicity): The multiplicity of the property.
        visibility (str): The visibility of the property ('public', 'private', etc.).
        is_composite (bool): Indicates whether the property is a composite.
        is_navigable (bool): Indicates whether the property is navigable in a relationship.
        is_aggregation (bool): Indicates whether the property represents an aggregation.
    
    Raises:
        ValueError: (Invalid owner) if the owner is instance of DataType.
    """
    
    def __init__(self, name: str, owner: Type, property_type: Type, multiplicity: Multiplicity = Multiplicity(1, 1), visibility: str = 'public', 
                 is_composite: bool = False, is_navigable: bool = True, is_aggregation: bool = False):
        super().__init__(name, visibility)
        self.owner: Type = owner
        self.type: Type = property_type
        self.multiplicity: Multiplicity = multiplicity
        self.is_composite: bool = is_composite
        self.is_navigable: bool = is_navigable
        self.is_aggregation: bool = is_aggregation

    @property
    def owner(self) -> Type:
        """Type: Get the owner type of the property."""
        return self.__owner

    @owner.setter
    def owner(self, owner: Type):
        """Type: Set the owner type of the property. The owner cannot be a datatype."""
        if isinstance(owner, DataType):
            raise ValueError("Invalid owner")
        self.__owner = owner

    @property
    def type(self) -> Type:
        """Type: Get the property type."""
        return self.__type

    @type.setter
    def type(self, property_type: Type):
        """Type: Set the property type."""
        self.__type = property_type

    @property
    def multiplicity(self) -> Multiplicity:
        """Multiplicity: Get the multiplicity of the property."""
        return self.__multiplicity

    @multiplicity.setter
    def multiplicity(self, multiplicity: Multiplicity):
        """Multiplicity: Set the multiplicity of the property."""
        self.__multiplicity = multiplicity

    @property
    def is_composite(self) -> bool:
        """bool: Get wheter the property is composite."""
        return self.__is_composite

    @is_composite.setter
    def is_composite(self, is_composite: bool):
        """bool: Set wheter the property is composite."""
        self.__is_composite = is_composite

    @property
    def is_navigable(self) -> bool:
        """bool: Get wheter the property is navigable."""
        return self.__is_navigable

    @is_navigable.setter
    def is_navigable(self, is_navigable: bool):
        """bool: Set wheter the property is navigable."""
        self.__is_navigable = is_navigable

    @property
    def is_aggregation(self) -> bool:
        """bool: Get wheter the property represents an aggregation."""
        return self.__is_aggregation

    @is_aggregation.setter
    def is_aggregation(self, is_aggregation: bool):
        """bool: Set wheter the property represents an aggregation."""
        self.__is_aggregation = is_aggregation

    def __repr__(self):
        return f'Property({self.name},{self.visibility},{self.type},{self.multiplicity},{self.is_composite})'

class Class(Type):
    """Represents a class in a modeling context.

    A Class is a type that defines a blueprint for objects. It can have attributes, associations,
    and generalizations with other classes.

    Args:
        name (str): The name of the class.
        attributes (set[Property]): The set of attributes associated with the class.
        is_abstract (bool): Indicates whether the class is abstract.

    Attributes:
        name (str): The name of the class.
        attributes (set[Property]): The set of attributes associated with the class.
        is_abstract (bool): Indicates whether the class is abstract.
        __associations: Set of associations involving the class.
        __generalizations: Set of generalizations involving the class.
    
    Raises:
        ValueError: if two attributes have the same name.
    """

    def __init__(self, name: str, attributes: set[Property], is_abstract: bool= False):
        super().__init__(name)
        self.is_abstract: bool = is_abstract
        self.attributes: set[Property] = attributes
        self.__associations: set[Association] = set()
        self.__generalizations: set[Generalization] = set()

    @property
    def attributes(self) -> set[Property]:
        """set[Property]: Get the attributes of the class."""
        return self.__attributes

    @attributes.setter
    def attributes(self, attributes: set[Property]):
        """set[Property]: Set the attributes of the class. Attributes must have unique names"""
        if attributes is not None:
            names = [attribute.name for attribute in attributes]
            if len(names) != len(set(names)):
                raise ValueError("A class cannot have two attributes with the same name")
            for attribute in attributes:
                attribute.owner = self
            self.__attributes = attributes
        else:
            self.__attributes = set()

    def all_attributes(self) -> set[Property]:
        """set[Property]: Get all attributes, including inherited ones."""
        inherited_attributes: set[Property] = self.get_inherited_attributes()
        return self.__attributes | inherited_attributes

    def add_attribute(self, attribute: Property):
        """Property: Add an attribute to the list of class attributes. The attribute name must be unique"""
        if self.attributes is not None:
            if attribute.name in [attribute.name for attribute in self.attributes]:
                raise ValueError("A class cannot have two attributes with the same name")
        attribute.owner = self
        self.attributes.add(attribute)
    
    @property
    def is_abstract(self) -> bool:
        """bool: Get wheter the class is abstract."""
        return self.__is_abstract

    @is_abstract.setter
    def is_abstract(self, is_abstract: bool):
        """bool: Set wheter the class is abstract."""
        self.__is_abstract = is_abstract

    @property
    def associations(self):
        """set[Association]: Get the set of associations involving the class."""
        return self.__associations
    
    def _add_association(self, association):
        """Association: Add an association to the list of class associations."""
        self.__associations.add(association)
    
    def _delete_association(self, association):
        """Association: Remove an association to the list of class associations."""
        self.__associations.discard(association)

    @property
    def generalizations(self):
        """set[Generalization]: Get the set of generalizations involving the class."""
        return self.__generalizations
    
    def _add_generalization(self, generalization):
        """Generalization: Add a generalization to the list of class generalizations."""
        self.__generalizations.add(generalization)

    def _delete_generalization(self, generalization):
        """Generalization: Remove a generalization to the list of class generalizations."""
        self.__generalizations.discard(generalization)

    def get_inherited_attributes(self) -> set[Property]:
        """set[Property]: Get the list of inherited attributes."""
        for generalization in self.__generalizations:
            if (self == generalization.specific):
                inherited_attributes: set[Property] = generalization.general.attributes
                return inherited_attributes
        return set()
    
    def __repr__(self):
        return f'Class({self.name},{self.attributes})'

class Association(NamedElement):
    """Represents an association between classes.

    An Association defines a relationship between classes and is composed of two or more ends,
    each associated with a class. An association must have more than one end.

    Args:
        name (str): The name of the association.
        ends (set[Property]): The set of ends associated with the association.
        
    Attributes:
        name (str): The name of the association.
        ends (set[Property]): The set of ends associated with the association.

    Raises:
        ValueError: if an association has less than two ends.
    """

    def __init__(self, name: str, ends: set[Property]):
        super().__init__(name)
        self.ends: set[Property] = ends

    @property
    def ends(self) -> set[Property]:
        """set[Property]: Get the ends of the association."""
        return self.__ends

    @ends.setter
    def ends(self, ends: set[Property]):
        """set[Property]: Set the ends of the association. Two or more ends are required"""
        if len(ends) <= 1:
            raise ValueError("An association must have more than one end")
        if hasattr(self, "ends"):
            for end in self.ends:
                end.type._delete_association(association=self)
        for end in ends:
            end.owner = self
            end.type._add_association(association=self)
        self.__ends = ends

class BinaryAssociation(Association):
    """Represents a binary association between two classes.

    A BinaryAssociation is a specialized form of Association that specifically involves
    two ends, each associated with a class. It enforces constraints on the association,
    such as having exactly two ends. Exactly two ends are required 

    Args:
        name (str): The name of the binary association.
        ends (set[Property]): The set of ends associated with the binary association. 

    Attributes:
        name (str): The name of the binary association.
        ends (set[Property]): The set of ends associated with the binary association.
    
    Raises:
        ValueError: if the associaiton ends are not exactly two.
        ValueError: if both ends are tagged as agregation.
        ValueError: if both ends are tagged as composition.
    """

    def __init__(self, name: str, ends: set[Property]):
        super().__init__(name, ends)

    @Association.ends.setter
    def ends(self, ends: set[Property]):
        """set[Property]: Set the ends of the association. Two ends are required. Both ends 
        cannot be tagged as aggregation. Both ends cannot be tagged as composition."""
        if len(ends) != 2:
            raise ValueError("A binary must have exactly two ends")
        if list(ends)[0].is_aggregation == True and list(ends)[1].is_aggregation == True:
            raise ValueError("The aggregation attribute cannot be tagged at both ends")
        if list(ends)[0].is_composite == True and list(ends)[1].is_composite == True:
            raise ValueError("The composition attribute cannot be tagged at both ends")
        super(BinaryAssociation, BinaryAssociation).ends.fset(self, ends)

class AssociationClass(Class):
    # Class that has an association nature
    """An AssociationClass is a class that that has an association nature.
    It inherits from Class and is associated with an underlying Association.

    Args:
        name (str): The name of the association class.
        attributes (set[Property]): The set of attributes associated with the association class.
        association (Association): The underlying association linked to the association class.

    Attributes:
        name (str): The name of the association class.
        attributes (set[Property]): The set of attributes associated with the association class.
        association (Association): The underlying association linked to the association class.
    """

    def __init__(self, name: str, attributes: set[Property], association: Association):
        super().__init__(name, attributes)
        self.association: Association = association

    @property
    def association(self) -> Association:
        """Association: Get the underlying association of the association class."""
        return self.__association

    @association.setter
    def association(self, association: Association):
        """Association: Set the underlying association of the association class."""
        self.__association = association

class Generalization(Element):
    """Represents a generalization relationship between two classes.

    A Generalization is a relationship between two classes, where one class (specific)
    inherits attributes and behaviors from another class (general).

    Args:
        general (Class): The general (parent) class in the generalization relationship.
        specific (Class): The specific (child) class in the generalization relationship.
    
    Attributes:
        general (Class): The general (parent) class in the generalization relationship.
        specific (Class): The specific (child) class in the generalization relationship.

    Raises:
        ValueError: if the general class is equal to the specific class
    """

    def __init__(self, general: Class, specific: Class):
        self.general: Class = general
        self.specific: Class = specific

    @property
    def general(self) -> Class:
        """Class: Get the general (parent) class."""
        return self.__general

    @general.setter
    def general(self, general: Class):
        """Class: Set the general (parent) class."""
        if hasattr(self, "general"):
            self.general._delete_generalization(generalization=self)
        general._add_generalization(generalization=self)
        self.__general = general

    @property
    def specific(self) -> Class:
        """Class: Get the specific (child) class."""
        return self.__specific

    @specific.setter
    def specific(self, specific: Class):
        """Class: Set the specific (child) class. Specific cannot be the same class as general"""
        if specific == self.general:
            raise ValueError("you cannot have your own parent")
        if hasattr(self, "specific"):
            self.specific._delete_generalization(generalization=self)
        specific._add_generalization(generalization=self)
        self.__specific = specific

    def __repr__(self):
        return f'Generalization({self.general},{self.specific})'

class GeneralizationSet(NamedElement):
    """Represents a set of generalization relationships.

    Args:
        name (str): The name of the generalization set.
        generalizations (set[Generalization]): The set of generalization relationships in the set.
        is_disjoint (bool): Indicates whether the set is disjoint (instances cannot belong to more than one class in the set).
        is_complete (bool): Indicates whether the set is complete (every instance of the superclass must belong to a subclass).

    Attributes:
        name (str): The name of the generalization set.
        generalizations (set[Generalization]): The set of generalization relationships in the set.
        is_disjoint (bool): Indicates whether the set is disjoint (instances cannot belong to more than one class in the set).
        is_complete (bool): Indicates whether the set is complete (every instance of the superclass must belong to a subclass).
    """

    def __init__(self, name: str, generalizations: set[Generalization], is_disjoint: bool, is_complete: bool):
        super().__init__(name)
        self.generalizations: set[Generalization] = generalizations
        self.is_disjoint: bool = is_disjoint
        self.is_complete: bool = is_complete

    @property
    def generalizations(self) -> set[Generalization]:
        """set[Generalization]: Get the generalization relationships."""
        return self.__generalizations

    @generalizations.setter
    def generalizations(self, generalizations: set[Generalization]):
        """set[Generalization]: Set the generalization relationships."""
        self.__generalizations = generalizations

    @property
    def is_disjoint(self) -> bool:
        """bool: Get whether the set is disjoint."""
        return self.__is_disjoint

    @is_disjoint.setter
    def is_disjoint(self, is_disjoint: bool):
        """bool: Set whether the set is disjoint."""
        self.__is_disjoint = is_disjoint

    @property
    def is_complete(self) -> bool:
        """bool: Get whether the set is complete."""
        return self.__is_complete

    @is_complete.setter
    def is_complete(self, is_complete: bool):
        """bool: Set whether the set is complete."""
        self.__is_complete = is_complete

class Package(NamedElement):
    """A Package is a grouping mechanism that allows organizing and managing a set of classes.

    Attributes:
        name (str): The name of the package.
        classes (set[Class]): The set of classes contained in the package.
    
    Attributes:
        name (str): The name of the package.
        classes (set[Class]): The set of classes contained in the package.
    """

    def __init__(self, name: str, classes: set[Class]):
        super().__init__(name)
        self.classes: set[Class] = classes

    @property
    def classes(self) -> set[Class]:
        """set[Class]: Get the classes contained in the package."""
        return self.__classes

    @classes.setter
    def classes(self, classes: set[Class]):
        """set[Class]: Set the classes contained in the package."""
        self.__classes = classes

class Constraint(NamedElement):
    """A Constraint is a statement that restricts or defines conditions on the behavior,
    structure, or other aspects of the modeled system.

    Args:
        name (str): The name of the constraint.
        context (Class): The class to which the constraint is associated.
        expression (str): The expression or condition defined by the constraint.
        language (str): The language in which the constraint expression is written.

    Attributes:
        name (str): The name of the constraint.
        context (Class): The class to which the constraint is associated.
        expression (str): The expression or condition defined by the constraint.
        language (str): The language in which the constraint expression is written.
    """
        
    def __init__(self, name: str, context: Class, expression: Any, language: str):
        super().__init__(name)
        self.context: Class = context
        self.expression: str = expression
        self.language: str = language

    @property
    def context(self) -> Class:
        """Class: Get the class to which the constraint is associated."""
        return self.__context

    @context.setter
    def context(self, context: Class):
        """Class: Set the class to which the constraint is associated."""
        self.__context = context

    @property
    def expression(self) -> str:
        """str: Get the expression or condition defined by the constraint."""
        return self.__expression

    @expression.setter
    def expression(self, expression: Any):
        """str: Set the expression or condition defined by the constraint."""
        self.__expression = expression

    @property
    def language(self) -> str:
        """str: Get the language in which the constraint expression is written."""
        return self.__language

    @language.setter
    def language(self, language: str):
        """str: Set the language in which the constraint expression is written."""
        self.__language = language

    def __repr__(self):
        return f'Constraint({self.name},{self.context.name},{self.language},{self.expression})'

class DomainModel(NamedElement):
    """A domain model is the root element that comprises a number of types, associations, 
    generalizations, packages, constraints, and others.

    Args:
        name (str): The name of the domain model.
        types (set[Type]): The set of types (classes and datatypes) in the domain model.
        packages (set[Package]): The set of packages in the domain model.
        constraints (set[Constraint]): The set of constraints in the domain model.
        associations (set[Association]): The set of associations in the domain model.
        generalizations (set[Generalization]): The set of generalizations in the domain model.

    Attributes:
        name (str): The name of the domain model.
        types (set[Type]): The set of types (classes and datatypes) in the domain model.
        packages (set[Package]): The set of packages in the domain model.
        constraints (set[Constraint]): The set of constraints in the domain model.
        associations (set[Association]): The set of associations in the domain model.
        generalizations (set[Generalization]): The set of generalizations in the domain model.

    Raises:
        ValueError: if there are two types with the same name
        ValueError: if there are two associations with the same name
        ValueError: if there are two packages with the same name
    """

    def __init__(self, name: str, types: set[Type] = None, associations: set[Association] = None, generalizations: set[Generalization] = None, packages: set[Package] = None, constraints: set[Constraint] = None):
        super().__init__(name)
        self.types: set[Type] = types
        self.packages: set[Package] = packages
        self.constraints: set[Constraint] = constraints
        self.associations: set[Association] = associations
        self.generalizations: set[Generalization] = generalizations

    @property
    def types(self) -> set[Type]:
        """set[Type]: Get the set of types in the domain model."""
        return self.__types

    @types.setter
    def types(self, types: set[Type]):
        """set[Type]: Set the set of types in the domain model. The model cannot contain
         two types with the same name."""
        if types is not None:
            names = [type.name for type in types]
            if len(names) != len(set(names)):
                raise ValueError("The model cannot have two types with the same name")
            self.__types = types
        else:
            self.__types = set()

    @property
    def associations(self) -> set[Association]:
        """set[Association]: Get the set of associations in the domain model."""
        return self.__associations

    @associations.setter
    def associations(self, associations: set[Association]):
        """set[Association]: Set the set of associations in the domain model. The model 
        cannot contain two associations with the same name."""
        if associations is not None:
            names = [association.name for association in associations]
            if len(names) != len(set(names)):
                raise ValueError("The model cannot have two associations with the same name")
            self.__associations = associations
        else:
            self.__associations = set()

    @property
    def generalizations(self) -> set[Generalization]:
        """set[Generalization]: Get the set of generalizations in the domain model."""
        return self.__generalizations

    @generalizations.setter
    def generalizations(self, generalizations: set[Generalization]):
        """set[Generalization]: Set the set of generalizations in the domain model."""
        if generalizations is not None:
            self.__generalizations = generalizations
        else:
            self.__generalizations = set()

    @property
    def packages(self) -> set[Package]:
        """set[Package]: Get the set of packages in the domain model."""
        return self.__packages

    @packages.setter
    def packages(self, packages: set[Package]):
        """set[Package]: Get the set of packages in the domain model. The model 
        cannot contain two packages with the same name."""
        if packages is not None:
            names = [package.name for package in packages]
            if len(names) != len(set(names)):
                raise ValueError("The model cannot have two packages with the same name")
            self.__packages = packages
        else:
            self.__packages = set()

    @property
    def constraints(self) -> set[Constraint]:
        """set[Constraint]: Get the set of constraints in the domain model."""
        return self.__constraints

    @constraints.setter
    def constraints(self, constraints: set[Constraint]):
        """set[Constraint]: Get the set of constraints in the domain model. The model 
        cannot contain two constraints with the same name."""
        if constraints is not None:
            names = [constraint.name for constraint in constraints]
            if len(names) != len(set(names)):
                raise ValueError("The model cannot have two constraints with the same name")
            self.__constraints = constraints
        else:
            self.__constraints = set()

    def get_classes(self) -> set[Class]:
        """set[Class]: Get all classes within the domain model."""
        return {element for element in self.types if isinstance(element, Class)}
    
    def get_class_by_name(self, class_name: str) -> Class:
        """Class: Gets a class by name."""
        return next((element for element in self.types if isinstance(element, Class) and element.name == class_name), None)