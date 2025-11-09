from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets


class PasswordResetToken(models.Model):
    """
    Model to store password reset tokens.
    
    Tokens are single-use and expire after a certain period.
    This prevents token reuse and limits the time window for password reset.
    """
    
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        verbose_name="User",
        help_text="User who requested password reset"
    )
    
    token = models.CharField(
        verbose_name="Token",
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Unique password reset token string"
    )
    
    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        help_text="When this token was created"
    )
    
    expires_at = models.DateTimeField(
        verbose_name="Expires at",
        help_text="When this token expires"
    )
    
    is_used = models.BooleanField(
        verbose_name="Used",
        default=False,
        db_index=True,
        help_text="Whether this token has been used"
    )
    
    used_at = models.DateTimeField(
        verbose_name="Used at",
        null=True,
        blank=True,
        help_text="When this token was used"
    )
    
    ip_address = models.GenericIPAddressField(
        verbose_name="IP address",
        null=True,
        blank=True,
        help_text="IP address from which reset was requested"
    )
    
    class Meta:
        verbose_name = "Password Reset Token"
        verbose_name_plural = "Password Reset Tokens"
        ordering = ["-created_at"]
        db_table = "password_reset_tokens"
        indexes = [
            models.Index(fields=["token", "is_used"]),
            models.Index(fields=["user", "is_used", "expires_at"]),
            models.Index(fields=["expires_at"]),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.token[:20]}..."
    
    def is_valid(self):
        """
        Check if the token is valid (not expired and not used).
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        if self.is_used:
            return False
        
        if timezone.now() > self.expires_at:
            return False
        
        if not self.user.is_active:
            return False
        
        return True
    
    def mark_as_used(self):
        """
        Mark this token as used.
        """
        if not self.is_used:
            self.is_used = True
            self.used_at = timezone.now()
            self.save(update_fields=["is_used", "used_at"])
    
    @classmethod
    def generate_token(cls):
        """
        Generate a unique token string.
        
        Returns:
            str: Unique token string
        """
        return secrets.token_urlsafe(32)
    
    @classmethod
    def create_token(cls, user, ip_address=None, expires_in_hours=24):
        """
        Create a new password reset token for a user.
        Invalidates all previous unused tokens for this user.
        
        Args:
            user: User instance
            ip_address: Optional IP address
            expires_in_hours: Number of hours until expiration (default: 24)
        
        Returns:
            PasswordResetToken: Created token instance
        """
        # Invalidate all previous unused tokens for this user
        cls.objects.filter(
            user=user,
            is_used=False
        ).update(is_used=True, used_at=timezone.now())
        
        token_string = cls.generate_token()
        expires_at = timezone.now() + timedelta(hours=expires_in_hours)
        
        token = cls.objects.create(
            user=user,
            token=token_string,
            expires_at=expires_at,
            ip_address=ip_address
        )
        
        return token
    
    @classmethod
    def cleanup_expired_tokens(cls):
        """
        Delete all expired tokens from the database.
        Should be run periodically (e.g., via cron job or celery task).
        
        Returns:
            int: Number of tokens deleted
        """
        count, _ = cls.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()
        return count
