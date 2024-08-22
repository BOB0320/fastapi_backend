import json

from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound


from src.models.db.onboarding import Onboarding
from src.models.db.user import User
from src.models.schemas.onboarding import OnboardingRequest, OnboardingFeedback
from src.repository.crud.base import BaseCRUDRepository


class OnboardingCRUDRepository(BaseCRUDRepository):    
    async def create_or_update_onboarding(self, onboarding_create: OnboardingRequest) -> None:
        async with self.async_session as session:
            try:
                async with session.begin():
                    result = await session.execute(
                        select(Onboarding)
                        .where(Onboarding.user_id == onboarding_create.userId)
                    )
                    existing_onboarding = result.scalars().first()
                    
                    items_list = list(onboarding_create.items)
                    detailed_qa_list = [item.to_dict() for item in items_list]  # Convert to list of dicts
                    detailed_qa_serialized = json.dumps(detailed_qa_list)  # Serialize to JSON
                    
                    if existing_onboarding:
                        existing_onboarding.primary_personality = onboarding_create.primaryPersonality
                        existing_onboarding.specific_personality = onboarding_create.specificPersonality
                        existing_onboarding.detailed_qa = detailed_qa_serialized
                        new_onboarding=None
                    else:
                        # Create a new onboarding record
                        new_onboarding = Onboarding(
                            user_id=onboarding_create.userId,
                            primary_personality=onboarding_create.primaryPersonality,
                            specific_personality=onboarding_create.specificPersonality,
                            detailed_qa = detailed_qa_serialized
                        )
                        session.add(new_onboarding)
                
                # Fetch the corresponding user record and update the onboarding status
                result = await session.execute(
                    select(User).where(User.id == onboarding_create.userId)
                )
                user = result.scalars().first()
                
                if user:
                    user.is_onboarding = False
                else:
                    raise NoResultFound(f"User with ID not found.")
                
                # Commit the transaction if everything went well
                await session.commit()
                # Refresh the newly created onboarding record if it was created
                if new_onboarding:
                    await session.refresh(new_onboarding)
                                
            except NoResultFound:
                raise NoResultFound(f"User with ID not found.")
            except ValueError as ve:
                # Rollback and raise ValueError
                await session.rollback()
                raise ValueError(f"Invalid data: {str(ve)}")
            except Exception as e:
                # Rollback and raise any other unexpected errors
                await session.rollback()
                raise SystemError(f"Unexpected error during onboarding save: {str(e)}")
             
                    
    async def save_feedback(self, feedback_create: OnboardingFeedback) -> None:
        async with self.async_session as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(Onboarding)
                        .where(Onboarding.user_id == feedback_create.userId)
                    )
                    onboarding = result.scalars().first()

                    if onboarding:
                        onboarding.feedback = feedback_create.feedback
                        session.add(onboarding)
                    else:
                        raise NoResultFound(f"User with ID not found.")
                    
                except NoResultFound:
                    raise NoResultFound(f"User with ID not found.")
                except ValueError as ve:
                    # Rollback and raise ValueError
                    await session.rollback()
                    raise ValueError(f"Invalid data: {str(ve)}")
                except Exception as e:
                    # Rollback and raise any other unexpected errors
                    await session.rollback()
                    raise SystemError(f"Unexpected error during feedback save: {str(e)}")
                
            await session.commit()