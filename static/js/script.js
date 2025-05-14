// Dropdown functionality for project selector
document.addEventListener('DOMContentLoaded', function() {
    const projectDropdown = document.querySelector('.project-dropdown button');
  

    if (projectDropdown) {
        projectDropdown.addEventListener('click', function() {
            // This would toggle a dropdown menu in a real implementation
            console.log('Project dropdown clicked');
        });
    }
    
    // Change plan button functionality
    const changePlanBtn = document.querySelector('.change-plan-btn');
    
    if (changePlanBtn) {
        changePlanBtn.addEventListener('click', function() {
            // Scroll to pricing section
            const pricingSection = document.querySelector('.pricing-section');
            if (pricingSection) {
                pricingSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
    
    // Cancel subscription button
    const cancelBtn = document.querySelector('.cancel-btn');
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {

            const payPalSubscriptionId = this.dataset.subscriptionId; // Get ID from data attribute
        
            if (!payPalSubscriptionId) {
                alert('Error: Subscription ID not found. Cannot cancel.');
                return;
            }

            if (confirm('Are you sure you want to cancel your subscription?')) {
                console.log('Initiating cancellation for PayPal Subscription ID:', payPalSubscriptionId);


                // This would handle the PayPal cancellation in a real implementation #ak47
                
                fetch(cancelURL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // Sending JSON
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        paypal_subscription_id: payPalSubscriptionId,
                        reason: 'User requested cancellation via website.' // Optional reason
                    })
                }).then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                    // Try to get error message from server response if JSON
                    return response.json().then(errData => {
                        throw new Error(errData.error || `Server error: ${response.status}`);
                    }).catch(() => {
                        // Fallback if response isn't JSON or doesn't have .error
                        throw new Error(`Failed to cancel subscription. Server responded with ${response.status}`);
                    });
                }
                }).then(data => {
                    if (data.success) {
                        alert('Subscription cancelled successfully!');
                        window.location.reload(); // Or redirect to a confirmation page
                    } else {
                        alert('Failed to cancel subscription: ' + (data.error || 'Unknown error from server.'));
                    }
                }).catch(function (err) {
                    // Hide loading indicator
                    console.error("Cancellation request failed:", err);
                    alert("An error occurred while trying to cancel your subscription: " + err.message);
                });
                // This would handle the PayPal cancellation in a real implementation #ak47

                // This would handle subscription cancellation in a real implementation
            }
        });
    }
    
    // Choose plan buttons
    const choosePlanBtns = document.querySelectorAll('.choose-btn');
    
    if (choosePlanBtns) {
        choosePlanBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const planName = this.closest('.pricing-card').querySelector('h3').textContent;
                
                const selectedPlanId = this.getAttribute('data-plan-id');

                if (!selectedPlanId) {
                    alert('Error: Could not determine the selected plan.');
                    return;
                }

                console.log(`Selected Plan: ${planName} (ID: ${selectedPlanId})`);
                console.log(`Current Subscription ID: ${currentSubscriptionId}, Current Plan ID: ${currentPlanId}`);


            // If user already has a subscription, update it
            if (currentSubscriptionId && currentSubscriptionId !== 'None' && currentSubscriptionId !== null && selectedPlanId !== currentPlanId) {
                    if (!confirm(`You're about to change your current plan to ${planName}. This change will typically take effect on your next billing cycle. Continue?`)) {
                        return;
                    }

                                        // Show loading indicator
                    // document.getElementById('loading-indicator').style.display = 'block';


                fetch(updateUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                            current_paypal_subscription_id: currentSubscriptionId,
                            new_paypal_plan_id: selectedPlanId
                    })
                })                    .then(response => {
                        // Hide loading indicator
                        // document.getElementById('loading-indicator').style.display = 'none';
                        if (!response.ok) {
                             // Try to parse error from JSON response
                            return response.json().then(errData => {
                                throw new Error(errData.error || `Server error: ${response.status}`);
                            }).catch(() => {
                                // Fallback if response isn't JSON
                                throw new Error(`Failed to change plan. Server responded with ${response.status}`);
                            });
                        }
                        return response.json();
                    })
                    .then(result => {
                        if (result.success) {
                            alert("Plan change request submitted successfully! The change will reflect on your next billing cycle.");
                            window.location.reload();
                        } else {
                            alert("Failed to change plan: " + (result.error || "Unknown server error."));
                        }
                    })
                    .catch(error => {
                        // Hide loading indicator
                        // document.getElementById('loading-indicator').style.display = 'none';
                        console.error('Error changing plan:', error);
                        alert('An error occurred while changing your plan: ' + error.message);
                    });

                } else if (!currentSubscriptionId || currentSubscriptionId === 'None' || currentSubscriptionId === null) {
                    // Else, if no current subscription, render PayPal button for new subscription
                    console.log('No active subscription. Rendering PayPal button for new subscription with plan ID:', selectedPlanId);
                    document.getElementById('paypal-button-container').innerHTML = ''; // Clear previous button
                    paypal.Buttons({
                        createSubscription: function (data, actions) {
                            return actions.subscription.create({
                                plan_id: selectedPlanId
                                // You can add 'custom_id': '{{ request.user.id }}' here if user is logged in
                                // and your save_subscription_view is prepared to handle it for user linking,
                                // especially if webhook might create the record.
                            });
                        },

                        onApprove: function (data) {
                            fetch(saveUrl, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': csrfToken
                                },
                                body: JSON.stringify({
                                    subscriptionID: data.subscriptionID,
                                    planID: selectedPlanId // send the selected planID
                                })
                            }).then(response => response.json())
                              .then(result => {
                                  if (result.success) {
                                      alert('Subscription created successfully!');
                                      window.location.reload();
                                  } else {
                                      alert('New subscription failed: ' + (result.error || "Unknown server error."));
                                  }
                              }).catch(error => {
                                  console.error('Error saving new subscription:', error);
                                  alert('Error saving new subscription.');
                              });
                        },
                        onError: function(err) {
                            console.error('PayPal Buttons error:', err);
                            alert('An error occurred with PayPal. Please try again.');
                        }
                    }).render('#paypal-button-container');
                } else if (selectedPlanId === currentPlanId) {
                    alert("You are already subscribed to this plan.");
                }
            });
        });
    }
    
    // Sidebar navigation highlighting
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    
    if (sidebarLinks) {
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Remove active class from all links
                sidebarLinks.forEach(l => l.parentElement.classList.remove('active'));
                
                // Add active class to clicked link
                this.parentElement.classList.add('active');
            });
        });
    }
});