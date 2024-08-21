import typing
import loguru

from sqlalchemy.future import select
from src.models.db.onboarding import Onboarding
from src.models.db.user import User
from src.models.schemas.onboarding import OnboardingRequest, OnboardingFeedback
from src.repository.crud.base import BaseCRUDRepository


class OnboardingCRUDRepository(BaseCRUDRepository):
    async def create_onboarding(self, onboarding_create: OnboardingRequest) -> bool:
        try:
            async with self.async_session as session:
                try:
                    async with session.begin():
                        # Create a new onboarding record
                        new_onboarding = Onboarding(
                            user_id=onboarding_create.userId,
                            primary_personality=onboarding_create.primaryPersonality,
                            specific_personality=onboarding_create.specificPersonality,
                        )
                        session.add(new_onboarding)

                    # Commit and refresh in the same transaction
                    await session.commit()
                    await session.refresh(new_onboarding)
                except Exception as e:
                    await session.rollback()
                    print("**************", str(e))
                    return False

            # After the first transaction is complete, start a new one
            async with self.async_session as session:
                try:
                    async with session.begin():
                        # Fetch the corresponding user record
                        result = await session.execute(
                            select(User)
                            .where(User.id == onboarding_create.userId)
                        )
                        user = result.scalars().first()

                        # Update the onboarding status
                        if user:
                            user.is_onboarding = False
                            session.add(user)

                    # Commit the transaction if everything went well
                    await session.commit()

                    return True  # Return true only if the commit is successful

                except Exception as e:
                    # Rollback the transaction in case of an error
                    await session.rollback()
                    print("**************", str(e))
                    return False  # Return false if any error occurs
                
        except Exception as e:
            print("**************", str(e))
            return False
    
    async def save_feedback(self, feedback_create: OnboardingFeedback) -> bool:
        try:
            async with self.async_session as session:
                async with session.begin():
                    result = await session.execute(
                        select(Onboarding)
                        .where(Onboarding.user_id == feedback_create.userId)
                    )
                    onboarding = result.scalars().first()

                    # Update the onboarding status
                    if onboarding:
                        onboarding.feedback = feedback_create.feedback
                        session.add(onboarding)

                # Commit the transaction if everything went well
                await session.commit()
                return True
        except Exception as e:
            await session.rollback()
            print("**************", str(e))
            return False