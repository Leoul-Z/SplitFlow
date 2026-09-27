from rest_framework import serializers
# pyrefly: ignore [missing-import]
from .models import Expense, ExpenseSplit


class ExpenseSplitSerializer(serializers.ModelSerializer):
    share = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = ExpenseSplit
        fields = ['id', 'user', 'share']
        read_only_fields = ['id']


class ExpenseSerializer(serializers.ModelSerializer):
    splits = ExpenseSplitSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'created_at', 'paid_by', 'group', 'split_type', 'splits']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        amount = data.get('amount')
        split_type = data.get('split_type')
        splits = data.get('splits')

        if split_type == 'exact':
            total = sum(item['share'] for item in splits)
            if round(total, 2) != round(amount, 2):
                raise serializers.ValidationError({"splits": "Sum of splits does not equal the amount."})

        elif split_type == 'percentage':
            total = sum(item['share'] for item in splits)
            if round(total, 2) != 100:
                raise serializers.ValidationError({"splits": "Percentages must sum to 100."})

        else: 
            share_per_person = round(amount / len(splits), 2)
            for split in splits:
                split['share'] = share_per_person

        return data

    def create(self, validated_data):
        splits_data = validated_data.pop('splits')
        expense = Expense.objects.create(**validated_data)

        for split in splits_data:
            ExpenseSplit.objects.create(expense=expense, **split)

        return expense