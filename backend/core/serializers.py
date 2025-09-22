from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserMeSerializer(serializers.ModelSerializer):
    """
    Serializer para o endpoint /me/ (usuário autenticado).
    Retorna informações básicas do usuário logado.
    """
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'role']

class UserSummarySerializer(serializers.ModelSerializer):
    """
    Serializer para listagem básica de usuários.
    Retorna id, email, first_name, last_name, role e status ativo.
    """
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'is_active']

class UserFullSerializer(serializers.ModelSerializer):
    """
    Serializer completo para criação e atualização de usuários.
    Permite definir email, first_name, last_name, role e senha.
    """
    password = serializers.CharField(write_only=True, required=False, min_length=6)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    role = serializers.ChoiceField(choices=User.role.field.choices, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'password', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def to_representation(self, instance):
        """
        Extrai nomes do email automaticamente ao serializar.
        """
        if not instance.first_name and not instance.last_name and instance.email:
            instance.extract_names_from_email()
            instance.save()
        return super().to_representation(instance)
    
    def validate_email(self, value):
        """
        Valida se o email é único.
        """
        exclude_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=exclude_id).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value
    
    def validate_role(self, value):
        """
        Impede alteração da role do primeiro superuser criado.
        """
        if self.instance and self.instance.is_superuser:
            first_superuser = User.objects.filter(is_superuser=True).order_by('id').first()
            if first_superuser and self.instance.id == first_superuser.id:
                if value != self.instance.role:
                    raise serializers.ValidationError("Não é possível alterar a role do administrador padrão.")
        return value
    
    def validate_is_active(self, value):
        """
        Impede desativação do primeiro superuser criado.
        """
        if self.instance and self.instance.is_superuser and not value:
            first_superuser = User.objects.filter(is_superuser=True).order_by('id').first()
            if first_superuser and self.instance.id == first_superuser.id:
                raise serializers.ValidationError("Não é possível desativar o administrador padrão.")
        return value
    
    def create(self, validated_data):
        """
        Cria usuário com senha criptografada e gera email automaticamente.
        """
        password = validated_data.pop('password', None)
        
        first_name = validated_data.get('first_name', '').lower()
        last_name = validated_data.get('last_name', '').lower()
        first_name = self._remove_accents(first_name)
        last_name = self._remove_accents(last_name)
        validated_data['email'] = f"{first_name}.{last_name}@metalaluminio.com.br"
        
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def _remove_accents(self, text):
        """
        Remove acentos de uma string.
        """
        import unicodedata
        return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    
    def update(self, instance, validated_data):
        """
        Atualiza usuário, tratando senha separadamente.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

